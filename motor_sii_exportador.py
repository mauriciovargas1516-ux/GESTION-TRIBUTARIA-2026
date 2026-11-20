# -*- coding: utf-8 -*-
"""
motor_sii_exportador.py
Motor tributario auxiliar y exportador Excel (.xlsx) con formulas nativas activas
para Gestion Tributaria 2026 (ULagos).
"""

import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


# Tabla de tramos Impuesto Unico de Segunda Categoria (en UTM)
TRAMOS_IUSC_UTM = [
    (0.0, 13.5, 0.00, 0.00),
    (13.5, 30.0, 0.04, 0.54),
    (30.0, 50.0, 0.08, 1.74),
    (50.0, 70.0, 0.135, 4.49),
    (70.0, 90.0, 0.23, 11.14),
    (90.0, 120.0, 0.304, 17.80),
    (120.0, 310.0, 0.35, 23.32),
    (310.0, float("inf"), 0.40, 38.82),
]


def calcular_impuesto_unico_2da_cat(renta_tributable_clp: float, valor_utm: float) -> dict:
    """Calcula el Impuesto Unico de Segunda Categoria usando tramos legales en UTM."""
    if valor_utm <= 0 or renta_tributable_clp <= 0:
        return {
            "renta_utm": 0.0,
            "tramo": "Exento (0 a 13,5 UTM)",
            "factor": 0.0,
            "rebaja_utm": 0.0,
            "impuesto_utm": 0.0,
            "impuesto_clp": 0.0,
            "tasa_efectiva_pct": 0.0,
            "liquido_estimado_clp": max(0.0, renta_tributable_clp),
        }

    renta_utm = renta_tributable_clp / valor_utm
    for desde, hasta, factor, rebaja in TRAMOS_IUSC_UTM:
        if desde <= renta_utm <= hasta:
            imp_utm = max(0.0, (renta_utm * factor) - rebaja)
            imp_clp = imp_utm * valor_utm
            etq_hasta = f"{hasta:.1f}" if hasta != float("inf") else "y mas"
            return {
                "renta_utm": renta_utm,
                "tramo": f"{desde:.1f} a {etq_hasta} UTM",
                "factor": factor,
                "rebaja_utm": rebaja,
                "impuesto_utm": imp_utm,
                "impuesto_clp": imp_clp,
                "tasa_efectiva_pct": (imp_clp / renta_tributable_clp) * 100.0,
                "liquido_estimado_clp": renta_tributable_clp - imp_clp,
            }

    return {
        "renta_utm": renta_utm,
        "tramo": "N/A",
        "factor": 0.0,
        "rebaja_utm": 0.0,
        "impuesto_utm": 0.0,
        "impuesto_clp": 0.0,
        "tasa_efectiva_pct": 0.0,
        "liquido_estimado_clp": renta_tributable_clp,
    }


def tabla_tramos_iusc_df(valor_utm: float) -> pd.DataFrame:
    """Retorna la tabla de tramos del Impuesto Unico expresada en UTM y CLP."""
    filas = []
    for desde, hasta, factor, rebaja in TRAMOS_IUSC_UTM:
        filas.append({
            "Desde (UTM)": desde,
            "Hasta (UTM)": "Mas de 310" if hasta == float("inf") else hasta,
            "Desde ($ CLP)": round(desde * valor_utm),
            "Hasta ($ CLP)": "Sin tope" if hasta == float("inf") else round(hasta * valor_utm),
            "Factor (%)": f"{factor * 100:.1f}%",
            "Rebaja (UTM)": rebaja,
            "Rebaja ($ CLP)": round(rebaja * valor_utm),
        })
    return pd.DataFrame(filas)


def exportar_libros_y_f29_excel(datos_f29: dict) -> bytes:
    """
    Genera un libro Excel (.xlsx) en estilo monocromatico ejecutivo con formulas nativas:
      1. Resumen F29 (Liquidacion IVA, Proporcionalidad y Remanente UTM)
      2. Libro Ventas (Detalle base + formulas de IVA 19% y Total)
      3. Libro Compras (Incluye columna IVA Recuperable vs No Recuperable Art. 23 N°4)
      4. Tramos IUSC (Tabla de Impuesto Unico 2da Categoria en UTM y CLP)
    """
    wb = Workbook()
    wb.remove(wb.active)

    fill_titulo = PatternFill("solid", fgColor="1E293B")
    fill_header = PatternFill("solid", fgColor="334155")
    fill_sub = PatternFill("solid", fgColor="E2E8F0")
    fill_total = PatternFill("solid", fgColor="CBD5E1")
    fill_calc = PatternFill("solid", fgColor="F8FAFC")
    fill_white = PatternFill("solid", fgColor="FFFFFF")

    font_titulo = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    font_sub = Font(name="Calibri", size=10, italic=True, color="334155")
    font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    font_reg = Font(name="Calibri", size=10, color="1E293B")

    borde = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )
    borde_tot = Border(
        left=Side(style="thin", color="94A3B8"),
        right=Side(style="thin", color="94A3B8"),
        top=Side(style="thin", color="0F172A"),
        bottom=Side(style="double", color="0F172A"),
    )

    def _banner(ws, n_cols, titulo, subtitulo):
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n_cols)
        c1 = ws.cell(1, 1, titulo)
        c1.fill, c1.font = fill_titulo, font_titulo
        c1.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[1].height = 25

        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n_cols)
        c2 = ws.cell(2, 1, subtitulo)
        c2.font = font_sub
        c2.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[2].height = 18

    def _autoajustar(ws, min_w=13, max_w=42):
        for col_idx in range(1, ws.max_column + 1):
            col_let = get_column_letter(col_idx)
            mx = 0
            for r in range(3, ws.max_row + 1):
                val = ws.cell(r, col_idx).value
                if val is not None and not str(val).startswith("="):
                    mx = max(mx, len(str(val)))
            ws.column_dimensions[col_let].width = max(min(mx + 4, max_w), min_w)

    # ------------------------------------------------------------------
    # HOJA 1: RESUMEN F29 (FORMULAS VIVAS)
    # ------------------------------------------------------------------
    ws1 = wb.create_sheet("Resumen F29")
    _banner(
        ws1,
        4,
        "LIQUIDACION MENSUAL DE IVA (FORMULARIO 29) — DL N° 825",
        "Gestion Tributaria 2026 | Formulas nativas de Excel activas",
    )

    headers_1 = ["Codigo / Concepto", "Base Imponible / Dato", "IVA / Resultado", "Observacion Normativa"]
    for c_i, h in enumerate(headers_1, 1):
        cel = ws1.cell(4, c_i, h)
        cel.fill, cel.font, cel.border = fill_header, font_header, borde
        cel.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[4].height = 24

    filas_f29 = [
        ("Ventas y Servicios Afectos Netos", datos_f29["ventas_afectas_neto"], "=ROUND(B5*0.19,0)", "Art. 2 DL 825 — Debito Fiscal"),
        ("Notas de Debito Emitidas Netas (+)", datos_f29["notas_debito_neto"], "=ROUND(B6*0.19,0)", "Aumenta Debito Fiscal"),
        ("Notas de Credito Emitidas Netas (-)", datos_f29["notas_credito_neto"], "=-ROUND(B7*0.19,0)", "Disminuye Debito Fiscal"),
        ("Ventas Exentas / No Gravadas del Mes", datos_f29["ventas_exentas"], 0, "Afecta proporcionalidad"),
        ("TOTAL DEBITO FISCAL DEL MES", "=MAX(0,B5+B6-B7)", "=MAX(0,SUM(C5:C7))", "Base neta y Debito del periodo"),
        ("Ventas Afectas Acumuladas Anuales", datos_f29["acum_afectas"], None, "Para proporcionalidad acumulada"),
        ("Ventas Exentas Acumuladas Anuales", datos_f29["acum_exentas"], None, "Para proporcionalidad acumulada"),
        ("Coeficiente Proporcionalidad (%)", "=IF((B10+B11)>0,B10/(B10+B11),1)", None, "Art. 23 N° 3 DL 825"),
        ("Compras Afectas Exclusivas Giro Afecto", datos_f29["compras_giro_neto"], "=ROUND(B13*0.19,0)", "Credito Fiscal 100%"),
        ("Compras Afectas de Uso Comun", datos_f29["compras_uso_comun_neto"], "=ROUND(B14*0.19*B12,0)", "Credito proporcional"),
        ("Compras Giro Exento / Automoviles (Art. 23 N°4)", datos_f29["compras_exentas_vinculo"], 0, "IVA no recuperable (pasa a costo/gasto)"),
        ("Remanente Credito Fiscal Mes Anterior (UTM)", datos_f29["remanente_utm_ant"], "=ROUND(B16*B17,0)", "Reajustado a UTM del mes de pago"),
        ("Valor UTM Mes de Declaracion ($)", datos_f29["valor_utm"], None, "UTM oficial SII"),
        ("TOTAL CREDITO FISCAL IMPUTABLE", None, "=SUM(C13:C16)", "Total imputable contra Debito"),
        ("IVA No Recuperable (Costo / Gasto)", None, "=ROUND(B14*0.19*(1-B12),0)+ROUND(B15*0.19,0)", "Proporcion no usada + Art. 23 N°4"),
        ("DIFERENCIA (DEBITO - CREDITO)", None, "=C9-C18", "> 0: IVA a pagar | <= 0: Remanente"),
        ("IVA DETERMINADO A PAGAR EN F29 ($)", None, "=IF(C20>0,C20,0)", "Pago hasta dia 12 / 20"),
        ("REMANENTE CREDITO FISCAL NUEVO (UTM)", None, "=IF(C20<0,ROUND(ABS(C20)/B17,2),0)", "Se arrastra al mes siguiente en UTM"),
    ]

    for idx_f, (con, val_b, val_c, obs) in enumerate(filas_f29, start=5):
        es_tot = con.startswith(("TOTAL", "IVA DETERMINADO", "REMANENTE CREDITO FISCAL NUEVO"))
        c_a = ws1.cell(idx_f, 1, con)
        c_b = ws1.cell(idx_f, 2, val_b)
        c_c = ws1.cell(idx_f, 3, val_c)
        c_d = ws1.cell(idx_f, 4, obs)

        for col_k, cel in enumerate((c_a, c_b, c_c, c_d), 1):
            cel.border = borde_tot if es_tot else borde
            cel.font = font_bold if (es_tot or col_k == 1) else font_reg
            cel.fill = fill_total if es_tot else (fill_calc if isinstance(cel.value, str) and cel.value.startswith("=") else fill_white)

        c_a.alignment = Alignment(horizontal="left", vertical="center")
        c_d.alignment = Alignment(horizontal="left", vertical="center")
        c_b.alignment = Alignment(horizontal="right", vertical="center")
        c_c.alignment = Alignment(horizontal="right", vertical="center")

        if idx_f == 12:
            c_b.number_format = "0.00%"
        elif idx_f == 16:
            c_b.number_format = "#,##0.00"
        elif val_b is not None:
            c_b.number_format = '$#,##0;-$#,##0;"$0"'

        if idx_f == 22:
            c_c.number_format = "#,##0.00"
        elif val_c is not None:
            c_c.number_format = '$#,##0;-$#,##0;"$0"'

    ws1.freeze_panes = "A5"
    _autoajustar(ws1)

    # ------------------------------------------------------------------
    # HOJA 2: LIBRO DE VENTAS (RESUMEN CON FORMULAS)
    # ------------------------------------------------------------------
    ws2 = wb.create_sheet("Libro Ventas")
    _banner(ws2, 6, "LIBRO AUXILIAR DE VENTAS (RCV)", "Resumen de documentos emitidos del periodo")
    hdr_v = ["Tipo Documento", "Cantidad", "Neto ($)", "Exento ($)", "IVA 19% ($)", "Total Bruto ($)"]
    for i, h in enumerate(hdr_v, 1):
        c = ws2.cell(4, i, h)
        c.fill, c.font, c.border = fill_header, font_header, borde
        c.alignment = Alignment(horizontal="center", vertical="center")

    filas_v = [
        ("Facturas Electronicas (33)", 1, datos_f29["ventas_afectas_neto"], 0),
        ("Facturas Exentas (34)", 1, 0, datos_f29["ventas_exentas"]),
        ("Notas de Debito (56)", 1, datos_f29["notas_debito_neto"], 0),
        ("Notas de Credito (61)", 1, -datos_f29["notas_credito_neto"], 0),
    ]
    for r_i, (doc, cant, neto, exen) in enumerate(filas_v, start=5):
        ws2.cell(r_i, 1, doc).font = font_reg
        ws2.cell(r_i, 2, cant).alignment = Alignment(horizontal="center")
        ws2.cell(r_i, 3, neto).number_format = '$#,##0;-$#,##0;"$0"'
        ws2.cell(r_i, 4, exen).number_format = '$#,##0;-$#,##0;"$0"'
        ws2.cell(r_i, 5, f"=ROUND(C{r_i}*0.19,0)").number_format = '$#,##0;-$#,##0;"$0"'
        ws2.cell(r_i, 6, f"=C{r_i}+D{r_i}+E{r_i}").number_format = '$#,##0;-$#,##0;"$0"'
        for c_k in range(1, 7):
            ws2.cell(r_i, c_k).border = borde

    ws2.cell(9, 1, "TOTAL LIBRO VENTAS")
    for c_k in range(2, 7):
        let = get_column_letter(c_k)
        c = ws2.cell(9, c_k, f"=SUM({let}5:{let}8)")
        c.number_format = "#,##0" if c_k == 2 else '$#,##0;-$#,##0;"$0"'
    for c_k in range(1, 7):
        cel = ws2.cell(9, c_k)
        cel.fill, cel.font, cel.border = fill_total, font_bold, borde_tot
    _autoajustar(ws2)

    # ------------------------------------------------------------------
    # HOJA 3: LIBRO DE COMPRAS (CREDITO VS NO RECUPERABLE)
    # ------------------------------------------------------------------
    ws3 = wb.create_sheet("Libro Compras")
    _banner(ws3, 6, "LIBRO AUXILIAR DE COMPRAS (RCV)", "Separacion de IVA Credito Fiscal y Art. 23 N°4 DL 825")
    hdr_c = ["Clasificacion de Compra", "Neto ($)", "IVA Total 19% ($)", "IVA Recuperable ($)", "IVA No Recuperable ($)", "Total Factura ($)"]
    for i, h in enumerate(hdr_c, 1):
        c = ws3.cell(4, i, h)
        c.fill, c.font, c.border = fill_header, font_header, borde
        c.alignment = Alignment(horizontal="center", vertical="center")

    filas_c = [
        ("Compras Exclusivas Giro Afecto", datos_f29["compras_giro_neto"], "=C5", "=0"),
        ("Compras de Uso Comun (Proporcional)", datos_f29["compras_uso_comun_neto"], "=ROUND(C6*'Resumen F29'!$B$12,0)", "=C6-D6"),
        ("Compras Giro Exento / Automoviles Art. 23 N°4", datos_f29["compras_exentas_vinculo"], "=0", "=C7"),
    ]
    for r_i, (nom, neto, f_rec, f_norec) in enumerate(filas_c, start=5):
        ws3.cell(r_i, 1, nom).font = font_reg
        ws3.cell(r_i, 2, neto).number_format = '$#,##0;-$#,##0;"$0"'
        ws3.cell(r_i, 3, f"=ROUND(B{r_i}*0.19,0)").number_format = '$#,##0;-$#,##0;"$0"'
        ws3.cell(r_i, 4, f_rec).number_format = '$#,##0;-$#,##0;"$0"'
        ws3.cell(r_i, 5, f_norec).number_format = '$#,##0;-$#,##0;"$0"'
        ws3.cell(r_i, 6, f"=B{r_i}+C{r_i}").number_format = '$#,##0;-$#,##0;"$0"'
        for c_k in range(1, 7):
            ws3.cell(r_i, c_k).border = borde

    ws3.cell(8, 1, "TOTAL LIBRO COMPRAS")
    for c_k in range(2, 7):
        let = get_column_letter(c_k)
        c = ws3.cell(8, c_k, f"=SUM({let}5:{let}7)")
        c.number_format = '$#,##0;-$#,##0;"$0"'
    for c_k in range(1, 7):
        cel = ws3.cell(8, c_k)
        cel.fill, cel.font, cel.border = fill_total, font_bold, borde_tot
    _autoajustar(ws3)

    # ------------------------------------------------------------------
    # HOJA 4: TRAMOS IMPUESTO UNICO 2DA CATEGORIA
    # ------------------------------------------------------------------
    ws4 = wb.create_sheet("Tramos IUSC UTM")
    _banner(ws4, 6, "ESCALA IMPUESTO UNICO DE SEGUNDA CATEGORIA (UTM)", f"Valor UTM de referencia: ${datos_f29['valor_utm']:,.0f} CLP")
    hdr_u = ["Desde (UTM)", "Hasta (UTM)", "Desde ($ CLP)", "Hasta ($ CLP)", "Factor", "Rebaja (UTM)"]
    for i, h in enumerate(hdr_u, 1):
        c = ws4.cell(4, i, h)
        c.fill, c.font, c.border = fill_header, font_header, borde
        c.alignment = Alignment(horizontal="center", vertical="center")

    for r_i, (desde, hasta, factor, rebaja) in enumerate(TRAMOS_IUSC_UTM, start=5):
        ws4.cell(r_i, 1, desde).number_format = "0.0"
        ws4.cell(r_i, 2, "Sin tope" if hasta == float("inf") else hasta)
        ws4.cell(r_i, 3, f"=ROUND(A{r_i}*'Resumen F29'!$B$17,0)").number_format = '$#,##0'
        ws4.cell(r_i, 4, "Sin tope" if hasta == float("inf") else f"=ROUND(B{r_i}*'Resumen F29'!$B$17,0)")
        if hasta != float("inf"):
            ws4.cell(r_i, 2).number_format = "0.0"
            ws4.cell(r_i, 4).number_format = '$#,##0'
        ws4.cell(r_i, 5, factor).number_format = "0.0%"
        ws4.cell(r_i, 6, rebaja).number_format = "0.00"
        for c_k in range(1, 7):
            ws4.cell(r_i, c_k).border = borde
    _autoajustar(ws4)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()
