import io
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats


@st.cache_data(show_spinner=False)
def cargar_base_nacional_sii(archivo_subido=None):
    """Lee la base nacional del SII desde un archivo subido (.xlsx/.xlsb) o desde el Excel local del repo."""
    if archivo_subido is not None:
        nombre = archivo_subido.name.lower()
        if nombre.endswith(".xlsb"):
            df = pd.read_excel(archivo_subido, engine="pyxlsb")
        else:
            xls = pd.ExcelFile(archivo_subido)
            hoja = "Datos" if "Datos" in xls.sheet_names else xls.sheet_names[0]
            df = pd.read_excel(xls, hoja)
        return df

    for ruta in ["ILPES GRUPO 10 29-10-2026.xlsx", "ILPES GRUPO 10 TERRITORIAL AL 19-10-2026.xlsx"]:
        if os.path.exists(ruta):
            xls = pd.ExcelFile(ruta)
            if "Datos" in xls.sheet_names:
                return pd.read_excel(xls, "Datos")

    for arch in os.listdir("."):
        if arch.lower().endswith(".xlsb"):
            return pd.read_excel(arch, engine="pyxlsb")

    return None


def construir_matrices_region(df_raw, region_sel, anio_0, anio_t, col_variable):
    """Filtra la región seleccionada, limpia celdas censuradas con '*' y arma las matrices V0 y Vt."""
    df = df_raw.copy()
    df = df[
        (df["Región del domicilio o casa matriz"] == region_sel)
        & (df["Comuna del domicilio o casa matriz"] != "Sin Información")
        & (df["Rubro económico"] != "Sin información")
        & (df["Año Comercial"].isin([anio_0, anio_t]))
    ].copy()

    df["Valor_Limpio"] = pd.to_numeric(df[col_variable], errors="coerce").fillna(0.0)

    comunas = sorted(df["Comuna del domicilio o casa matriz"].dropna().unique())
    sectores = sorted(df["Rubro económico"].dropna().unique())

    df_0 = (
        df[df["Año Comercial"] == anio_0]
        .pivot_table(
            index="Rubro económico",
            columns="Comuna del domicilio o casa matriz",
            values="Valor_Limpio",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reindex(index=sectores, columns=comunas, fill_value=0.0)
    )

    df_t = (
        df[df["Año Comercial"] == anio_t]
        .pivot_table(
            index="Rubro económico",
            columns="Comuna del domicilio o casa matriz",
            values="Valor_Limpio",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reindex(index=sectores, columns=comunas, fill_value=0.0)
    )

    return df_0, df_t, comunas, sectores


def calcular_todo_el_ramo(df_0, df_t, anio_0, anio_t):
    """Calcula todas las matrices de análisis regional ILPES, Shift & Share y Convergencia REAT."""
    V0 = df_0.values.astype(float)
    Vt = df_t.values.astype(float)
    comunas = list(df_0.columns)
    sectores = list(df_0.index)
    T = max(1, int(anio_t - anio_0))

    tot_reg_0 = V0.sum(axis=0)
    tot_sec_0 = V0.sum(axis=1)
    tot_nac_0 = V0.sum()

    tot_reg_t = Vt.sum(axis=0)
    tot_sec_t = Vt.sum(axis=1)
    tot_nac_t = Vt.sum()

    # 1. Matriz de Porcentaje (P_ij)
    P0 = np.divide(V0, tot_reg_0, out=np.zeros_like(V0), where=tot_reg_0 != 0)
    Pt = np.divide(Vt, tot_reg_t, out=np.zeros_like(Vt), where=tot_reg_t != 0)
    P_nac_0 = tot_sec_0 / tot_nac_0 if tot_nac_0 != 0 else np.zeros_like(tot_sec_0)
    P_nac_t = tot_sec_t / tot_nac_t if tot_nac_t != 0 else np.zeros_like(tot_sec_t)

    # 2. Cociente de Localización (Q_ij)
    Q0 = np.divide(P0, P_nac_0[:, None], out=np.zeros_like(P0), where=P_nac_0[:, None] != 0)
    Qt = np.divide(Pt, P_nac_t[:, None], out=np.zeros_like(Pt), where=P_nac_t[:, None] != 0)

    # 3. Coeficiente de Especialización (Q_r) y Reestructuración (CR_r)
    diff_esp_0 = np.abs(P0 - P_nac_0[:, None])
    diff_esp_t = np.abs(Pt - P_nac_t[:, None])
    Qr_0 = 0.5 * np.sum(diff_esp_0, axis=0)
    Qr_t = 0.5 * np.sum(diff_esp_t, axis=0)

    diff_reest = np.abs(Pt - P0)
    CRr = 0.5 * np.sum(diff_reest, axis=0)

    # 4. Base Exportadora (X_ij, X_j, M_j)
    X0_mat = np.where(Q0 > 1, V0 - (V0 / np.where(Q0 > 1, Q0, 1.0)), 0.0)
    Xt_mat = np.where(Qt > 1, Vt - (Vt / np.where(Qt > 1, Qt, 1.0)), 0.0)
    X0_tot = X0_mat.sum(axis=0)
    Xt_tot = Xt_mat.sum(axis=0)
    M0 = np.divide(tot_reg_0, X0_tot, out=np.zeros_like(tot_reg_0), where=X0_tot != 0)
    Mt = np.divide(tot_reg_t, Xt_tot, out=np.zeros_like(tot_reg_t), where=Xt_tot != 0)

    # 5. Variación Intertemporal (rV_ij y rR_j)
    rV_mat = np.divide(Vt, V0, out=np.zeros_like(Vt), where=V0 != 0)
    rR_j = np.divide(tot_reg_t, tot_reg_0, out=np.zeros_like(tot_reg_t), where=tot_reg_0 != 0)

    # 6. Shift & Share (MADE Clásico y MADE Modificado)
    r_nac = tot_nac_t / tot_nac_0 if tot_nac_0 != 0 else 1.0
    r_sec = np.divide(tot_sec_t, tot_sec_0, out=np.ones_like(tot_sec_0), where=tot_sec_0 != 0)

    ET = tot_reg_t - tot_reg_0 * r_nac
    EE_mat = V0 * (r_sec[:, None] - r_nac)
    EE = np.sum(EE_mat, axis=0)
    ED_mat = Vt - V0 * r_sec[:, None]
    ED = ET - EE

    r_nac_inv = tot_nac_0 / tot_nac_t if tot_nac_t != 0 else 1.0
    r_sec_inv = np.divide(tot_sec_0, tot_sec_t, out=np.ones_like(tot_sec_t), where=tot_sec_t != 0)
    EI_mat = Vt * (r_nac_inv - r_sec_inv[:, None])
    EI = np.sum(EI_mat, axis=0)
    EM = EI - EE
    ERM = ET - EI

    # 7. Cuadrantes de Silva
    tasa_anual_com = (np.power(np.maximum(rR_j, 1e-9), 1.0 / T) - 1.0) * 100.0
    tasa_anual_reg = ((r_nac ** (1.0 / T)) - 1.0) * 100.0
    media_nivel_t = np.mean(tot_reg_t)

    cuadrantes = []
    for c_rate, v_niv in zip(tasa_anual_com, tot_reg_t):
        if c_rate >= tasa_anual_reg and v_niv >= media_nivel_t:
            cuadrantes.append("C1 (+ +): Ganadores")
        elif c_rate >= tasa_anual_reg and v_niv < media_nivel_t:
            cuadrantes.append("C2 (- +): En Marcha (Convergentes)")
        elif c_rate < tasa_anual_reg and v_niv < media_nivel_t:
            cuadrantes.append("C3 (- -): Estancados")
        else:
            cuadrantes.append("C4 (+ -): En Retroceso")

    df_resumen = pd.DataFrame({
        "Comuna": comunas,
        f"Total_{anio_0}": tot_reg_0,
        f"Total_{anio_t}": tot_reg_t,
        "Cuociente_Variación (rRj)": rR_j,
        "Tasa_Crec_Anual (%)": tasa_anual_com,
        "Cuadrante_Silva": cuadrantes,
        f"Especialización_Qr_{anio_0}": Qr_0,
        f"Especialización_Qr_{anio_t}": Qr_t,
        "Reestructuración (CRr)": CRr,
        f"Exportación_Básica_{anio_0} (Xj)": X0_tot,
        f"Exportación_Básica_{anio_t} (Xj)": Xt_tot,
        f"Multiplicador_{anio_0} (Mj)": M0,
        f"Multiplicador_{anio_t} (Mj)": Mt,
        "Efecto_Total (ET)": ET,
        "Efecto_Estructural (EE)": EE,
        "Efecto_Diferencial (ED)": ED,
        "Efecto_Inverso (EI)": EI,
        "Efecto_Est_Modificado (EM)": EM,
        "Efecto_Reg_Modificado (ERM)": ERM,
    })

    # 8. Indicadores REAT de Disparidad, Concentración y Convergencia entre Comunas
    y0_pos = np.where(tot_reg_0 > 0, tot_reg_0, 1.0)
    yt_pos = np.where(tot_reg_t > 0, tot_reg_t, 1.0)
    ln_y0 = np.log(y0_pos)
    ln_yt = np.log(yt_pos)
    g_anual = (ln_yt - ln_y0) / T
    N = len(comunas)

    slope, intercept, r_val, p_val, std_err = stats.linregress(ln_y0, g_anual)

    def calc_gini(x):
        xs = np.sort(np.maximum(x, 0.0))
        if xs.sum() == 0:
            return 0.0
        n = len(xs)
        cp = np.arange(0, n + 1) / n
        cq = np.concatenate([[0.0], np.cumsum(xs) / xs.sum()])
        return 1.0 - np.sum((cp[1:] - cp[:-1]) * (cq[1:] + cq[:-1]))

    s0 = y0_pos / y0_pos.sum()
    st_sh = yt_pos / yt_pos.sum()
    theil_0 = np.sum(s0 * np.log(N * s0))
    theil_t = np.sum(st_sh * np.log(N * st_sh))
    hhi_0 = np.sum(s0 ** 2)
    hhi_t = np.sum(st_sh ** 2)

    df_reat = pd.DataFrame([
        {"Indicador REAT": "Número de Comunas Analizadas (N)", str(anio_0): N, str(anio_t): N},
        {"Indicador REAT": "Promedio Comunal", str(anio_0): np.mean(tot_reg_0), str(anio_t): np.mean(tot_reg_t)},
        {"Indicador REAT": "Mediana Comunal", str(anio_0): np.median(tot_reg_0), str(anio_t): np.median(tot_reg_t)},
        {"Indicador REAT": "Desviación Estándar de Logaritmos (Convergencia Sigma)", str(anio_0): np.std(ln_y0, ddof=1), str(anio_t): np.std(ln_yt, ddof=1)},
        {"Indicador REAT": "Coeficiente de Variación en Niveles (CV)", str(anio_0): np.std(tot_reg_0, ddof=0) / np.mean(tot_reg_0), str(anio_t): np.std(tot_reg_t, ddof=0) / np.mean(tot_reg_t)},
        {"Indicador REAT": "Índice de Desigualdad de Gini", str(anio_0): calc_gini(tot_reg_0), str(anio_t): calc_gini(tot_reg_t)},
        {"Indicador REAT": "Índice de Entropía de Theil", str(anio_0): theil_0, str(anio_t): theil_t},
        {"Indicador REAT": "Índice Herfindahl-Hirschman (HHI)", str(anio_0): hhi_0, str(anio_t): hhi_t},
        {"Indicador REAT": "Comunas Equivalentes (1 / HHI)", str(anio_0): 1.0 / hhi_0 if hhi_0 > 0 else np.nan, str(anio_t): 1.0 / hhi_t if hhi_t > 0 else np.nan},
        {"Indicador REAT": "Pendiente Convergencia Beta Anual (β OLS)", str(anio_0): slope, str(anio_t): np.nan},
        {"Indicador REAT": "Bondad de Ajuste Regresión Beta (R²)", str(anio_0): r_val ** 2, str(anio_t): np.nan},
        {"Indicador REAT": "Valor p Bilateral (Significancia Beta)", str(anio_0): p_val, str(anio_t): np.nan},
    ])

    return {
        "df_resumen": df_resumen,
        "df_reat": df_reat,
        "df_0": df_0,
        "df_t": df_t,
        "P0": pd.DataFrame(P0, index=sectores, columns=comunas),
        "Pt": pd.DataFrame(Pt, index=sectores, columns=comunas),
        "Q0": pd.DataFrame(Q0, index=sectores, columns=comunas),
        "Qt": pd.DataFrame(Qt, index=sectores, columns=comunas),
        "X0": pd.DataFrame(X0_mat, index=sectores, columns=comunas),
        "Xt": pd.DataFrame(Xt_mat, index=sectores, columns=comunas),
        "rV": pd.DataFrame(rV_mat, index=sectores, columns=comunas),
        "CRr_mat": pd.DataFrame(diff_reest, index=sectores, columns=comunas),
        "ED_mat": pd.DataFrame(ED_mat, index=sectores, columns=comunas),
        "EE_mat": pd.DataFrame(EE_mat, index=sectores, columns=comunas),
        "EI_mat": pd.DataFrame(EI_mat, index=sectores, columns=comunas),
    }


def compilar_excel_10_hojas(res_calc, anio_0, anio_t):
    """Empaqueta todos los indicadores del curso en un archivo Excel (.xlsx) descargable de 10 hojas."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        res_calc["df_resumen"].to_excel(writer, sheet_name="1_Resumen_ILPES_MADE", index=False)
        res_calc["df_reat"].to_excel(writer, sheet_name="2_Convergencia_REAT", index=False)
        res_calc["df_0"].to_excel(writer, sheet_name=f"3_Base_{anio_0}")
        res_calc["df_t"].to_excel(writer, sheet_name=f"4_Base_{anio_t}")
        res_calc["Pt"].to_excel(writer, sheet_name=f"5_Matriz_Porcentaje_{anio_t}")
        res_calc["Qt"].to_excel(writer, sheet_name=f"6_Cociente_Localiz_{anio_t}")
        res_calc["Xt"].to_excel(writer, sheet_name=f"7_Base_Exportadora_{anio_t}")
        res_calc["rV"].to_excel(writer, sheet_name="8_Coef_Variacion")
        res_calc["CRr_mat"].to_excel(writer, sheet_name="9_Reestructuracion")

        df_made_sheet = pd.concat([
            res_calc["ED_mat"].assign(Efecto="Efecto Diferencial (ED)"),
            res_calc["EE_mat"].assign(Efecto="Efecto Estructural (EE)"),
            res_calc["EI_mat"].assign(Efecto="Efecto Estructural Inverso (EI)"),
        ])
        df_made_sheet.to_excel(writer, sheet_name="10_Desglose_MADE_Sectorial")

    return buffer.getvalue()


def renderizar_modulo_nacional_sii(archivo_subido=None):
    """Renderiza en Streamlit el generador multi-región y exportador maestro de Excel."""
    st.markdown(
        "<div class='sec-header'>6. GENERADOR NACIONAL SII (16 REGIONES) Y EXPORTADOR MAESTRO A EXCEL</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "Construye y descarga automáticamente el libro de cálculo completo de la asignatura (**ILPES, Cuadrantes de Silva, "
        "Base Exportadora, Shift & Share MADE / Modificado y Convergencia REAT**) para **cualquiera de las 16 regiones de Chile** "
        "a partir de la estadística oficial del SII (`PUB_COMU_RUBR`)."
    )

    df_sii = cargar_base_nacional_sii(archivo_subido)
    if df_sii is None:
        st.warning("No se detectó la hoja 'Datos' en el repositorio. Sube el archivo del SII en el panel lateral.")
        return

    regiones_disp = sorted([
        r for r in df_sii["Región del domicilio o casa matriz"].dropna().unique()
        if r != "Sin Información"
    ])
    anios_disp = sorted([int(a) for a in df_sii["Año Comercial"].dropna().unique()])
    variables_disp = [
        "Ventas anuales en UF",
        "Número de empresas",
        "Número de trabajadores dependientes informados",
        "Renta neta informada en UF",
        "Trabajadores ponderados por meses trabajados",
    ]

    c1, c2, c3, c4 = st.columns([2.2, 1.8, 1.0, 1.0])
    idx_lagos = regiones_disp.index("Región de Los Lagos") if "Región de Los Lagos" in regiones_disp else 0
    region_sel = c1.selectbox("1. Seleccione Región de Chile:", regiones_disp, index=idx_lagos)
    var_sel = c2.selectbox("2. Variable Económica SII:", variables_disp, index=0)
    anio_0 = c3.selectbox("3. Año Inicial (t0):", anios_disp, index=anios_disp.index(2014) if 2014 in anios_disp else 0)
    anio_t = c4.selectbox("4. Año Final (t1):", anios_disp, index=anios_disp.index(2024) if 2024 in anios_disp else len(anios_disp) - 1)

    df_0, df_t, comunas, sectores = construir_matrices_region(df_sii, region_sel, anio_0, anio_t, var_sel)
    res_calc = calcular_todo_el_ramo(df_0, df_t, anio_0, anio_t)

    df_res = res_calc["df_resumen"]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Comunas en la Región", f"{len(comunas)} comunas")
    k2.metric(f"Total Regional ({anio_0})", f"{df_0.values.sum():,.0f}")
    k3.metric(f"Total Regional ({anio_t})", f"{df_t.values.sum():,.0f}")
    crec_reg = ((df_t.values.sum() / df_0.values.sum()) - 1.0) * 100.0 if df_0.values.sum() > 0 else 0.0
    k4.metric(f"Variación Acumulada ({anio_0}-{anio_t})", f"{crec_reg:.2f}%")

    excel_bytes = compilar_excel_10_hojas(res_calc, anio_0, anio_t)
    nombre_limpio = region_sel.replace(" ", "_").replace(".", "")
    st.download_button(
        label=f"Descargar Libro Excel Completo (10 Hojas) — {region_sel} ({anio_0}-{anio_t}).xlsx",
        data=excel_bytes,
        file_name=f"ILPES_REAT_{nombre_limpio}_{anio_0}_{anio_t}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )

    t_res, t_reat, t_made = st.tabs([
        "I. Tabla Maestra por Comuna (ILPES / MADE)",
        "II. Convergencia y Desigualdad Regional (REAT)",
        "III. Gráfico Shift & Share Regional",
    ])

    with t_res:
        st.dataframe(df_res.round(3), use_container_width=True, hide_index=True)
    with t_reat:
        st.dataframe(res_calc["df_reat"].round(4), use_container_width=True, hide_index=True)
    with t_made:
        fig_m = px.bar(
            df_res,
            x="Comuna",
            y=["Efecto_Estructural (EE)", "Efecto_Diferencial (ED)"],
            barmode="relative",
            title=f"Descomposición Shift & Share ({region_sel}: {anio_0} vs {anio_t})",
        )
        st.plotly_chart(fig_m, use_container_width=True)
