import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA - EXCLUSIVO GESTIÓN TRIBUTARIA 2026
# ==============================================================================
st.set_page_config(
    page_title="Gestión Tributaria para la Toma de Decisiones 2026 - ULagos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo Corporativo Limpio (Conservando paleta de colores ejecutiva sin emojis)
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem !important;}
    .corp-banner {
        background: linear-gradient(90deg, #0F172A 0%, #1E3A8A 100%);
        color: #FFFFFF;
        padding: 18px 24px;
        border-radius: 6px;
        margin-bottom: 18px;
        border-left: 5px solid #38BDF8;
    }
    .corp-title {font-size: 21px; font-weight: 700; margin: 0; letter-spacing: 0.3px;}
    .corp-sub {font-size: 13px; color: #CBD5E1; margin-top: 4px;}
    .sec-header {
        background-color: #DBEAFE;
        color: #1E3A8A;
        padding: 8px 14px;
        font-weight: 700;
        font-size: 14px;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 12px;
        border-left: 4px solid #1D4ED8;
    }
    button[data-baseweb="tab"] {font-weight: 600 !important;}
    </style>
    <div class="corp-banner">
        <div class="corp-title">SUITE DE GESTIÓN TRIBUTARIA PARA LA TOMA DE DECISIONES 2026</div>
        <div class="corp-sub">Motor Normativo, Simulador de Impuestos (DL 825 / LIR) y Analítica de Cumplimiento PGCT 2026 | ULagos</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# BASES DE CONOCIMIENTO Y DATOS NORMATIVOS SII CHILE (2025-2026)
# ==============================================================================
HITOS_HISTORIA_SII = [
    {"Año": "1902", "Norma / Hito": "Ley N° 1.515 (Pdte. Germán Riesco)", "Detalle": "Crea la Administración de los Impuestos sobre Alcoholes, precursora del SII."},
    {"Año": "1912", "Norma / Hito": "Dirección General de Impuestos", "Detalle": "Amplía fiscalización a tabaco, barajas, timbres, estampillas y espectáculos."},
    {"Año": "1916", "Norma / Hito": "Dirección General de Impuestos Internos", "Detalle": "Incorpora el cobro y aplicación de tributos a la propiedad territorial (contribuciones)."},
    {"Año": "1969", "Norma / Hito": "Creación del RUT (DFL)", "Detalle": "Establece el Rol Único Tributario como sistema de identificación nacional a cargo del SII."},
    {"Año": "1972", "Norma / Hito": "Servicio de Impuestos Internos (SII)", "Detalle": "Primer reglamento orgánico moderno y adopción del nombre definitivo SII."},
    {"Año": "2001", "Norma / Hito": "Ley N° 19.738 Antievasión", "Detalle": "Modifica Código Tributario, LIR, LIVS y leyes orgánicas de SII, Aduanas y TGR."},
    {"Año": "2012", "Norma / Hito": "Ley N° 20.630", "Detalle": "Perfecciona el artículo 21 de la LIR sobre retiros en especies y gastos rechazados."},
    {"Año": "2014", "Norma / Hito": "Ley N° 20.780 Reforma Tributaria", "Detalle": "Reforma estructural de los regímenes de tributación empresarial y recaudación fiscal."},
    {"Año": "2017", "Norma / Hito": "Transformación Digital SII", "Detalle": "Lanzamiento de Propuesta F29 y ecosistema móvil (e-RUT, e-Boleta, e-Renta, e-Reevalúo)."},
    {"Año": "2020", "Norma / Hito": "Ley N° 21.210 Modernización Tributaria", "Detalle": "Crea regímenes Pro Pyme General (14 D N°3), Transparente (14 D N°8) y Semi Integrado (14 A)."},
    {"Año": "2024", "Norma / Hito": "Ley N° 21.713 Cumplimiento Tributario", "Detalle": "Crea Consejo Tributario, multijurisdicción, sostenibilidad tributaria y refuerza persecución penal."},
]

ETAPAS_CICLO_VIDA = [
    {"Paso": "Paso 1: Obtención de RUT", "Plazo Legal": "Al completar constitución legal", "Sujetos Obligados": "Personas jurídicas y extranjeros sin residencia (personas naturales con RUN se registran automáticamente).", "Canal": "sii.cl"},
    {"Paso": "Paso 2: Inicio de Actividades", "Plazo Legal": "Dentro de los 2 meses siguientes al mes de inicio de operaciones", "Sujetos Obligados": "Toda entidad o persona natural que inicie actividades de 1ª Categoría (capital) o 2ª Categoría (trabajo).", "Canal": "sii.cl / App Móvil"},
    {"Paso": "Paso 3: Obligaciones Tributarias", "Plazo Legal": "Mensual (F29: día 12, 20 o 28) y Anual (F22: abril)", "Sujetos Obligados": "Contribuyentes activos (emisión de DTE, Registro de Compras y Ventas, DJ y pago de impuestos).", "Canal": "sii.cl"},
    {"Paso": "Paso 4: Solicitudes y Avisos Varios", "Plazo Legal": "Dentro de plazos de prescripción o cuando ocurra el hecho", "Sujetos Obligados": "Contribuyentes que requieran ampliación de giro, peticiones administrativas (RAF/RAV), condonaciones, etc.", "Canal": "sii.cl"},
    {"Paso": "Paso 5: Término de Giro", "Plazo Legal": "Dentro de los 2 meses siguientes al cese total de actividades", "Sujetos Obligados": "Todo contribuyente que ponga fin a su giro comercial o industrial y deje de estar afecto a impuestos.", "Canal": "sii.cl"},
]

DERECHOS_CONTRIBUYENTE_8BIS = [
    "1° Ser informado de sus derechos.",
    "2° Ser atendido en forma cortés, diligente y oportuna.",
    "3° Obtener en forma completa y oportuna las devoluciones a que tenga derecho.",
    "4° Que el SII indique razones, alcance, plazos de su actuación y certifique el término de la revisión.",
    "5° No ser fiscalizado nuevamente por los mismos hechos e impuestos ya revisados (Art. 59 Código Tributario).",
    "6° Conocer el nombre del funcionario(a) a cargo de su proceso.",
    "7° Obtener copias electrónicas o certificaciones de todas las actuaciones realizadas.",
    "8° Eximirse de aportar documentos ya entregados al SII y obtener devolución de originales.",
    "9° Respeto a la vida privada, protección de datos personales y reserva tributaria de las declaraciones.",
    "10° Actuaciones sin demoras innecesarias y en la forma menos costosa para el contribuyente.",
    "11° Presentar recursos, alegaciones o antecedentes personalmente o mediante representante.",
    "12° Plantear sugerencias y quejas respetuosas sobre las actuaciones del Servicio.",
    "13° Certeza jurídica de que los efectos tributarios de sus actos o contratos son los previstos por ley.",
    "14° Que las actuaciones del SII no entraben el normal desarrollo de las operaciones económicas.",
    "15° Ser notificado de cualquier restricción para informar actos o modificaciones (Arts. 68 y 69 CT).",
    "16° Recibir información sobre todas las anotaciones practicadas por el SII.",
    "17° Realizar rectificaciones necesarias salvo exclusiones legales.",
    "18° Respeto irrestricto a los plazos legales de prescripción y caducidad tributaria.",
    "19° Presunción legal de buena fe del contribuyente.",
    "20° Comparecencia remota o digital y facilidades electrónicas para quienes carezcan de medios tecnológicos.",
]

# ==============================================================================
# BARRA LATERAL Y NAVEGACIÓN
# ==============================================================================
st.sidebar.title("Gestión Tributaria 2026")
st.sidebar.markdown("**Universidad de Los Lagos**  \nIngeniería Comercial | Semestre X  \nDocente: Richard Arnoldo Villanueva Soto")
st.sidebar.divider()

modulo_trib = st.sidebar.radio(
    "Módulos del Sistema Tributario:",
    [
        "1. Institucionalidad, Ciclo de Vida y Derechos (CT)",
        "2. Clasificador y Simulador de Rentas (1ª vs 2ª Categoría)",
        "3. Simulador IVA, Proporcionalidad y Auditoría F29 (DL 825)",
        "4. Analítica PGCT 2026: Fiscalización, Brechas y Riesgo SII",
    ],
)

# ==============================================================================
# MÓDULO 1: INSTITUCIONALIDAD, CICLO DE VIDA Y DERECHOS DEL CONTRIBUYENTE
# ==============================================================================
if modulo_trib.startswith("1."):
    st.markdown("<div class='sec-header'>1. EDUCACIÓN FISCAL, ADMINISTRACIÓN TRIBUTARIA Y CICLO DE VIDA DEL CONTRIBUYENTE</div>", unsafe_allow_html=True)

    t1, t2, t3 = st.tabs([
        "I. Ecosistema Hacienda y Evolución SII",
        "II. Las 5 Etapas del Ciclo de Vida",
        "III. Derechos (Art. 8 bis / ter / quáter) y Deberes",
    ])

    with t1:
        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
        col_i1.info("**Ministerio de Hacienda**\nDirección estratégica de recursos públicos, estabilidad macroeconómica y política fiscal.")
        col_i2.success("**Servicio de Impuestos Internos (SII)**\nAplicación y fiscalización de impuestos internos (Renta, IVA, Territorial) y facilitación digital.")
        col_i3.warning("**Tesorería General de la República (TGR)**\nRecaudación, custodia y distribución de los recursos del Tesoro Público.")
        col_i4.error("**Servicio Nacional de Aduanas (SNA)**\nFiscalización del comercio exterior, aranceles y Declaraciones de Ingreso (DIN).")

        st.subheader("Línea de Tiempo Normativa e Institucional del SII (1902 – 2024)")
        st.dataframe(pd.DataFrame(HITOS_HISTORIA_SII), use_container_width=True, hide_index=True)

    with t2:
        st.subheader("Matriz Operativa del Ciclo de Vida del Contribuyente")
        st.dataframe(pd.DataFrame(ETAPAS_CICLO_VIDA), use_container_width=True, hide_index=True)

        st.markdown("**Verificador Rápido de Plazos Legales (Inicio y Término de Giro - Art. 68 y 69 CT)**")
        meses_lista = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        mes_evento = st.selectbox("Mes en que inició operaciones o cesó actividades:", meses_lista, index=9)
        idx_m = meses_lista.index(mes_evento)
        mes_limite = meses_lista[(idx_m + 2) % 12]
        st.success(f"Cálculo de plazo legal: Si el hecho ocurrió en **{mes_evento}**, el plazo legal vence el **último día hábil de {mes_limite}** (dentro de los 2 meses siguientes).")

    with t3:
        c_der, c_deb = st.columns([3, 2])
        with c_der:
            st.subheader("Catálogo de los 20 Derechos del Contribuyente (Art. 8 bis CT)")
            busqueda_der = st.text_input("Filtrar derecho por palabra clave (ej. fiscalización, buena fe, devolución):", "")
            derechos_filtrados = [d for d in DERECHOS_CONTRIBUYENTE_8BIS if busqueda_der.lower() in d.lower()]
            for d in derechos_filtrados:
                st.markdown(f"- {d}")
            st.caption("**Art. 8 ter y 8 quáter:** Derecho a autorización de documentos tributarios necesarios para el giro y obligación del SII de publicar en 'MiSII' cualquier restricción.")
        with c_deb:
            st.subheader("9 Deberes Legales del Contribuyente")
            st.markdown(
                "1. **Declarar y pagar impuestos** (Art. 18 CT y Art. 64 LIVS).\n"
                "2. **Mantener actualizado contacto y domicilio** (Art. 11 bis CT).\n"
                "3. **Formalizar emprendimientos** (Art. 68 CT).\n"
                "4. **Conservar documentación tributaria** (Art. 58 LIVS).\n"
                "5. **Proporcionar información requerida** (Art. 68 CT).\n"
                "6. **Trato respetuoso al personal** (Art. 90 Estatuto Adm.).\n"
                "7. **Cero violencia o acoso** (Ley Karin).\n"
                "8. **Cuidar instalaciones públicas** (Arts. 484-487 Código Penal).\n"
                "9. **Conocer la legislación vigente** (Art. 8 Código Civil)."
            )

# ==============================================================================
# MÓDULO 2: CLASIFICADOR Y SIMULADOR DE RENTAS (1ª CATEGORÍA VS 2ª CATEGORÍA)
# ==============================================================================
elif modulo_trib.startswith("2."):
    st.markdown("<div class='sec-header'>2. CLASIFICACIÓN TRIBUTARIA DE LAS RENTAS Y ESTRUCTURA JURÍDICA</div>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.subheader("Comparador: Empresario Individual vs. Persona Jurídica")
        df_figuras = pd.DataFrame({
            "Atributo Legal y Tributario": [
                "Conformación", "Constitución Legal", "Rol Único Tributario (RUT)",
                "Responsabilidad Patrimonial", "Exigencia de Capital Inicial", "Figuras Típicas"
            ],
            "Persona Natural (Empresario Individual)": [
                "1 sola persona natural", "No requiere escritura social", "Usa el mismo RUN personal",
                "Ilimitada (responde con patrimonio personal)", "No requiere acreditar capital mínimo",
                "Empresa Individual / Microempresa Familiar (MEF)"
            ],
            "Persona Jurídica (Sociedad / EIRL)": [
                "1 o más personas naturales o jurídicas", "Requiere escritura e inscripción legal",
                "RUT propio e independiente de los socios", "Limitada al capital o bienes de la empresa",
                "Requiere aporte de capital en dinero o bienes", "SpA, Ltda., S.A., EIRL, Soc. Colectiva"
            ],
        })
        st.dataframe(df_figuras, use_container_width=True, hide_index=True)

    with col_r2:
        st.subheader("Simulador de Rentas: Primera vs. Segunda Categoría")
        tipo_renta = st.selectbox(
            "Selecciona el origen de la renta a evaluar:",
            [
                "1ª Categoría: Industria, Comercio, Minería, Constructora o Inmobiliaria (Predomina Capital)",
                "2ª Categoría Independiente: Boleta de Honorarios Electrónica (Art. 42 N°2 LIR)",
                "2ª Categoría Dependiente: Sueldo Mensual bajo Contrato de Trabajo (Art. 42 N°1 LIR)",
            ],
        )
        monto_bruto = st.number_input("Monto Bruto del Período ($ CLP):", min_value=0, value=2500000, step=100000)

        if tipo_renta.startswith("1ª Categoría"):
            tasa_idpc = st.radio(
                "Régimen de Primera Categoría:",
                [12.5, 25.0, 27.0],
                index=1,
                format_func=lambda x: f"{x}% ({'Pro Pyme Transitorio' if x==12.5 else 'Pro Pyme General 14D3' if x==25.0 else 'Semi Integrado 14A'})",
                horizontal=True,
            )
            impuesto_est = monto_bruto * (tasa_idpc / 100.0)
            st.metric("Impuesto de Primera Categoría Estimado sobre RLI", f"${impuesto_est:,.0f} CLP", f"Tasa: {tasa_idpc}%")
            st.caption("Obligación documental: Factura Electrónica, Boleta de Ventas, Guía de Despacho, RCV, F29 y F22.")
        elif "Honorarios" in tipo_renta:
            tasa_ret = st.slider("Tasa de Retención Boleta de Honorarios (%):", min_value=10.0, max_value=17.0, value=15.25, step=0.75)
            retencion = monto_bruto * (tasa_ret / 100.0)
            liquido = monto_bruto - retencion
            st.metric("Monto Líquido a Recibir", f"${liquido:,.0f} CLP", f"Retención SII: ${retencion:,.0f} ({tasa_ret}%)")
            st.caption("Requisitos SII: Inicio de Actividades en 2ª Categoría, actividad del Art. 42 N°2 LIR y Clave Tributaria.")
        else:
            st.info("Los trabajadores dependientes tributan mediante el **Impuesto Único de Segunda Categoría** (escala progresiva por tramos en UTM), retenido y enterado mensualmente por el empleador en el F29 sin requerir Inicio de Actividades del trabajador.")

# ==============================================================================
# MÓDULO 3: SIMULADOR IVA, PROPORCIONALIDAD Y AUDITORÍA F29 (DL N° 825)
# ==============================================================================
elif modulo_trib.startswith("3."):
    st.markdown("<div class='sec-header'>3. IMPUESTO AL VALOR AGREGADO (DL N° 825): DÉBITO, CRÉDITO, PROPORCIONALIDAD Y F29</div>", unsafe_allow_html=True)

    iva_tab1, iva_tab2, iva_tab3 = st.tabs([
        "I. Determinación Mensual IVA, Proporcionalidad y Remanente UTM",
        "II. Calificador de Hecho Gravado en Servicios (Ley N° 21.420)",
        "III. Matriz de Auditoría Tributaria RCV - F29 y Checklist",
    ])

    with iva_tab1:
        st.subheader("Simulador de Liquidación Mensual de IVA (Formulario 29)")
        c_vta, c_cmp, c_res = st.columns(3)

        with c_vta:
            st.markdown("**1. Operaciones de Venta y Débito Fiscal**")
            ventas_afectas_neto = st.number_input("Ventas y Servicios Afectos Netos ($):", min_value=0, value=10000000, step=500000)
            ventas_exentas = st.number_input("Ventas y Servicios Exentos / No Gravados ($):", min_value=0, value=2000000, step=500000)
            notas_debito_neto = st.number_input(" (+) Notas de Débito Emitidas Netas ($):", min_value=0, value=0, step=100000)
            notas_credito_neto = st.number_input(" (-) Notas de Crédito Emitidas Netas ($):", min_value=0, value=0, step=100000)

            base_debito = max(0.0, ventas_afectas_neto + notas_debito_neto - notas_credito_neto)
            debito_fiscal = base_debito * 0.19
            total_ventas_mes = base_debito + ventas_exentas
            prop_afecta = (base_debito / total_ventas_mes * 100.0) if total_ventas_mes > 0 else 100.0

        with c_cmp:
            st.markdown("**2. Adquisiciones y Crédito Fiscal (RCV)**")
            compras_giro_neto = st.number_input("Compras Afectas Exclusivas del Giro Afecto ($):", min_value=0, value=6000000, step=500000)
            compras_uso_comun_neto = st.number_input("Compras Afectas de Uso Común ($):", min_value=0, value=3000000, step=500000)
            compras_exentas_vinculo = st.number_input("Compras Vinculadas a Giros Exentos ($):", min_value=0, value=500000, step=100000)
            remanente_utm_ant = st.number_input("Remanente Crédito Fiscal Mes Anterior (UTM):", min_value=0.0, value=0.0, step=1.0)
            valor_utm = st.number_input("Valor UTM del Mes de Declaración ($):", min_value=1000, value=67500, step=500)

            credito_directo = compras_giro_neto * 0.19
            iva_uso_comun_total = compras_uso_comun_neto * 0.19
            credito_uso_comun_recup = iva_uso_comun_total * (prop_afecta / 100.0)
            iva_no_recuperable = (iva_uso_comun_total - credito_uso_comun_recup) + (compras_exentas_vinculo * 0.19)
            remanente_pesos_ant = remanente_utm_ant * valor_utm
            credito_fiscal_total = credito_directo + credito_uso_comun_recup + remanente_pesos_ant

        with c_res:
            st.markdown("**3. Resultado Liquidación F29**")
            diferencia_iva = debito_fiscal - credito_fiscal_total
            st.metric("IVA Débito Fiscal del Mes", f"${debito_fiscal:,.0f} CLP")
            st.metric("IVA Crédito Fiscal Imputable", f"${credito_fiscal_total:,.0f} CLP", f"Proporcionalidad: {prop_afecta:.2f}%")
            if diferencia_iva > 0:
                st.error(f"**IVA Determinado a Pagar en F29:** ${diferencia_iva:,.0f} CLP")
            else:
                remanente_pesos = abs(diferencia_iva)
                remanente_utm_nuevo = remanente_pesos / valor_utm
                st.success(f"**Remanente de Crédito Fiscal:** ${remanente_pesos:,.0f} CLP ({remanente_utm_nuevo:.2f} UTM)")
            st.caption(f"IVA de compras que pasa a costo/gasto por proporcionalidad o giro exento: **${iva_no_recuperable:,.0f} CLP**.")

        st.divider()
        st.markdown("**Conversor Rápido Precio Neto / Precio Bruto con IVA (19%)**")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            monto_conv = st.number_input("Ingresa monto a convertir ($):", min_value=0, value=1190000, step=10000)
        with col_c2:
            modo_conv = st.radio("Tipo de monto ingresado:", ["Precio Total con IVA incluido (÷ 1,19)", "Precio Neto sin IVA (× 1,19)"])
        if modo_conv.startswith("Precio Total"):
            neto_calc = monto_conv / 1.19
            iva_calc = monto_conv - neto_calc
            st.info(f"**Neto:** ${neto_calc:,.0f} | **IVA (19%):** ${iva_calc:,.0f} | **Total Bruto:** ${monto_conv:,.0f}")
        else:
            iva_calc = monto_conv * 0.19
            total_calc = monto_conv + iva_calc
            st.info(f"**Neto:** ${monto_conv:,.0f} | **IVA (19%):** ${iva_calc:,.0f} | **Total Bruto:** ${total_calc:,.0f}")

    with iva_tab2:
        st.subheader("Árbol de Decisión: Tributación de Servicios desde Ley N° 21.420 (Arts. 2, 12 y 13 LIVS)")
        p1 = st.checkbox("1. ¿Existe una acción o prestación remunerada (interés, prima, comisión o precio)?", value=True)
        p2 = st.selectbox("2. ¿Quién presta el servicio?", [
            "Sociedad de Capital (SpA, S.A., Ltda. comercial/consultora)",
            "Sociedad de Profesionales registrada en el SII (cumple requisitos exclusivos)",
            "Persona Natural independiente (Emite Boleta de Honorarios)",
            "Establecimiento de Educación / Salud / Transporte de Pasajeros (Exenciones Arts. 12 y 13 LIVS)",
        ])
        if not p1:
            st.warning("Operación **No Gravada / No Afecta**: No se configura el hecho gravado básico de servicio.")
        elif "Sociedad de Capital" in p2:
            st.error("Operación **Afecta a IVA (19%)**: Desde el 1 de enero de 2023 todo servicio prestado por sociedades de capital se encuentra gravado con IVA, salvo exención expresa de los Arts. 12 o 13 de la LIVS.")
        else:
            st.success("Operación **Exenta de IVA**: Se emite documentación exenta o boleta de honorarios según corresponda; recordar que los ingresos exentos obligan a aplicar proporcionalidad sobre el IVA de compras de uso común.")

    with iva_tab3:
        st.subheader("Matriz de Control de Auditoría Tributaria y Plazos F29")
        df_aud_iva = pd.DataFrame([
            {"Etapa": "Ventas", "Pregunta de Control": "¿Todas las ventas afectas fueron documentadas?", "Evidencia": "DTE, RCV, vouchers POS, bancos, contratos", "Riesgo": "Débito fiscal omitido"},
            {"Etapa": "Compras", "Pregunta de Control": "¿El crédito fiscal cumple requisitos de la LIVS?", "Evidencia": "RCV, facturas válidas, acuse de recibo, giro", "Riesgo": "Crédito fiscal improcedente"},
            {"Etapa": "Devengo", "Pregunta de Control": "¿Se reconoció en el mes legalmente correcto?", "Evidencia": "Fecha emisión DTE, guías de despacho, entrega", "Riesgo": "Diferencias mensuales, reajustes y multas"},
            {"Etapa": "Notas NC/ND", "Pregunta de Control": "¿Están referenciadas y dentro de plazo?", "Evidencia": "Notas de Crédito/Débito y DTE original", "Riesgo": "IVA sobre o subdeclarado"},
            {"Etapa": "Formulario 29", "Pregunta de Control": "¿Cuadra RCV con libro mayor contable y F29?", "Evidencia": "F29, RCV, balance y mayor contable", "Riesgo": "Observaciones SII y rectificatorias"},
        ])
        st.dataframe(df_aud_iva, use_container_width=True, hide_index=True)
        st.info("**Plazos Generales F29:** Hasta el **día 12** del mes siguiente (regla general), **día 20** (declaración y pago electrónico por Internet para emisores de DTE según requisitos SII) y **día 28** (declaraciones sin movimiento / sin pago por Internet).")

# ==============================================================================
# MÓDULO 4: ANALÍTICA PGCT 2026: FISCALIZACIÓN, BRECHAS Y RIESGO SII
# ==============================================================================
elif modulo_trib.startswith("4."):
    st.markdown("<div class='sec-header'>4. PLAN DE GESTIÓN DE CUMPLIMIENTO TRIBUTARIO (PGCT 2026 - LEY N° 21.713)</div>", unsafe_allow_html=True)

    pg1, pg2, pg3 = st.tabs([
        "I. Fiscalización y Recaudación por Segmento",
        "II. Brechas de Evasión IVA y Control de Fraude",
        "III. Capacidades SII, Dotación y Formación PFI 2026",
    ])

    with pg1:
        st.subheader("Focalización del Modelo de Gestión de Cumplimiento Tributario (MGCT - Resultados 2025)")
        df_fisc = pd.DataFrame({
            "Segmento": ["Grandes Empresas", "Medianas Empresas", "Pequeñas Empresas", "Microempresas", "Altos Patrimonios", "Personas Naturales"],
            "Contribuyentes": [22159, 40493, 268776, 1175963, 106396, 4434679],
            "Auditorías": [2025, 1237, 1109, 473, 754, 293],
            "Revisiones_Cumplimiento": [1605, 1252, 4258, 3897, 1740, 1739],
            "Horas_Fiscalización": [250762, 138781, 129292, 70405, 94755, 38584],
            "Recaudación_MM_CLP": [37118913, 4486810, 4750790, 1738688, 3272817, 4068199],
        })
        df_fisc["%_Recaudación"] = (df_fisc["Recaudación_MM_CLP"] / df_fisc["Recaudación_MM_CLP"].sum() * 100).round(1)
        df_fisc["%_Horas_Fisc"] = (df_fisc["Horas_Fiscalización"] / df_fisc["Horas_Fiscalización"].sum() * 100).round(1)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Contribuyentes", "6.048.466", "+15,4% Inicios 1ª Cat. (215.064)")
        k2.metric("Recaudación Total (Nov 2025)", "$55.436.217 MM", "67% Grandes Empresas")
        k3.metric("Auditorías y Revisiones", "20.382", "5.891 Aud. + 14.491 Rev.")
        k4.metric("Autocorrección en Línea", "75,6%", "248.868 de 340.546 controlados")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fig_rec = px.pie(df_fisc, values="Recaudación_MM_CLP", names="Segmento", hole=0.4, title="Participación en la Recaudación Tributaria por Segmento")
            st.plotly_chart(fig_rec, use_container_width=True)
        with col_f2:
            fig_hrs = px.bar(df_fisc, x="Segmento", y=["%_Horas_Fisc", "%_Recaudación"], barmode="group", title="Focalización: % Horas de Fiscalización vs. % Recaudación")
            st.plotly_chart(fig_hrs, use_container_width=True)

        st.dataframe(df_fisc, use_container_width=True, hide_index=True)

    with pg2:
        st.subheader("Comparativa Internacional de Evasión de IVA y Combate al Delito Tributario")
        df_eva = pd.DataFrame({
            "País / Bloque": ["Perú", "Promedio América Latina", "Colombia", "Chile (2023)", "Italia", "Francia", "España", "Austria"],
            "Tasa_Evasión_IVA (%)": [32.2, 27.6, 23.6, 18.2, 14.7, 9.7, 7.1, 3.9],
        })
        fig_eva = px.bar(df_eva, x="Tasa_Evasión_IVA (%)", y="País / Bloque", orientation="h", color="Tasa_Evasión_IVA (%)", color_continuous_scale="RdYlGn_r", title="Tasa de Evasión de IVA Comparada (%)")
        st.plotly_chart(fig_eva, use_container_width=True)

        c_d1, c_d2, c_d3, c_d4 = st.columns(4)
        c_d1.metric("Nuevos Emisores Agresivos", "18.060", "+30,8% (Facturas falsas = 16,9% evasión IVA)")
        c_d2.metric("Crédito Fiscal Indebido Evitado", "$189.400 MM", "81.720 receptores detectados")
        c_d3.metric("Querellas y Denuncias 2025", "227 causas", "$158.000 MM perjuicio fiscal")
        c_d4.metric("Efectividad Sanción Penal", "80,5%", "136 de 169 causas con condena/salida")

    with pg3:
        st.subheader("Dotación Efectiva SII (4.913 Funcionarios) y Cobertura Plan de Formación (PFI 2026)")
        df_dot = pd.DataFrame({
            "Escalafón": ["Fiscalizador Tributario", "Profesional", "Administrativo", "Fiscalizador Tasador", "Técnico Fiscalizador", "Directivo", "Auxiliar", "Técnico Informática", "Técnico Avaluaciones"],
            "Funcionarios": [1774, 1354, 784, 329, 220, 218, 144, 68, 22],
        })
        df_pfi = pd.DataFrame({
            "Foco Formativo PFI 2026": [
                "Gestión de Cumplimiento Tributario",
                "Base Contable y Tributaria",
                "Liderazgo y Gestión de Equipos",
                "Directrices y Procedimientos Transversales",
                "Análisis de Datos y Gestión Digital",
            ],
            "Cupos": [5093, 1408, 1281, 923, 888],
        })
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.plotly_chart(px.bar(df_dot, x="Escalafón", y="Funcionarios", color="Funcionarios", title="Dotación SII por Escalafón (2.545 Mujeres / 2.368 Hombres)"), use_container_width=True)
        with col_p2:
            st.plotly_chart(px.pie(df_pfi, values="Cupos", names="Foco Formativo PFI 2026", hole=0.4, title="Distribución de los 9.593 Cupos PFI 2026"), use_container_width=True)
