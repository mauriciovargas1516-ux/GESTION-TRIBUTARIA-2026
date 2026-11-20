# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

import motor_sii_exportador as m_sii

# ==============================================================================
# CONFIGURACION DE PAGINA - SUITE GESTION TRIBUTARIA 2026
# ==============================================================================
st.set_page_config(
    page_title="Gestion Tributaria para la Toma de Decisiones 2026 - ULagos",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        <div class="corp-title">SUITE DE GESTION TRIBUTARIA PARA LA TOMA DE DECISIONES 2026</div>
        <div class="corp-sub">Motor Normativo, Simulador de Impuestos (DL 825 / LIR), Art. 97 CT, Exportador Excel y Entrenador | ULagos</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# BASES DE CONOCIMIENTO NORMATIVO SII CHILE
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
    {"Paso": "Paso 1: Obtención de RUT", "Plazo Legal": "Al completar constitución legal", "Sujetos Obligados": "Personas jurídicas y extranjeros sin residencia.", "Canal": "sii.cl"},
    {"Paso": "Paso 2: Inicio de Actividades", "Plazo Legal": "Dentro de los 2 meses siguientes al mes de inicio de operaciones", "Sujetos Obligados": "Toda entidad o persona natural que inicie actividades de 1ª o 2ª Categoría.", "Canal": "sii.cl / App Móvil"},
    {"Paso": "Paso 3: Obligaciones Tributarias", "Plazo Legal": "Mensual (F29: día 12, 20 o 28) y Anual (F22: abril)", "Sujetos Obligados": "Contribuyentes activos (DTE, RCV, DJ y pago de impuestos).", "Canal": "sii.cl"},
    {"Paso": "Paso 4: Solicitudes y Avisos Varios", "Plazo Legal": "Dentro de plazos de prescripción o cuando ocurra el hecho", "Sujetos Obligados": "Ampliación de giro, peticiones administrativas (RAF/RAV), condonaciones.", "Canal": "sii.cl"},
    {"Paso": "Paso 5: Término de Giro", "Plazo Legal": "Dentro de los 2 meses siguientes al cese total de actividades", "Sujetos Obligados": "Todo contribuyente que ponga fin a su giro comercial o industrial.", "Canal": "sii.cl"},
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

FORMULAS_MODO_CIEGO = [
    {
        "titulo": "1. Neto de una Boleta con IVA (19%)",
        "formula": r"\text{Neto} = \frac{\text{Total Bruto}}{1,19} \quad | \quad \text{IVA} = \text{Total Bruto} - \text{Neto}",
        "regla": "Nunca restes el 19% al total bruto; siempre divide por 1,19 para aislar la base neta.",
    },
    {
        "titulo": "2. Remanente de Crédito Fiscal en UTM",
        "formula": r"\text{Remanente UTM} = \frac{\text{Remanente CLP}}{\text{UTM}_{\text{mes de declaración}}}",
        "regla": "Se convierte a UTM con la UTM del mes en que corresponde pagar el F29 y se reajusta al mes siguiente.",
    },
    {
        "titulo": "3. Proporcionalidad de IVA de Uso Común (Art. 23 N° 3 DL 825)",
        "formula": r"\%\text{Proporcionalidad} = \frac{\text{Ventas Afectas Acumuladas}}{\text{Ventas Afectas Acum.} + \text{Ventas Exentas Acum.}}",
        "regla": "Se aplica de forma acumulada dentro del año calendario. La fracción no recuperable pasa a costo o gasto.",
    },
    {
        "titulo": "4. Exclusión de Automóviles (Art. 23 N° 4 DL 825)",
        "formula": r"\text{IVA Automóvil / Station Wagon} \rightarrow \text{IVA No Recuperable (0\% Crédito)}",
        "regla": "A diferencia de un furgón de reparto o una grúa horquilla, un automóvil particular no da derecho a crédito fiscal.",
    },
    {
        "titulo": "5. Delito Tributario por Facturas Falsas (Art. 97 N° 4 CT)",
        "formula": r"\text{Multa: } 50\%\text{ a }400\% \text{ del tributo eludido} + \text{Presidio}",
        "regla": "Obliga a restituir el IVA Crédito Fiscal indebido, rechaza el gasto en Renta (Art. 21 LIR) y genera responsabilidad penal.",
    },
    {
        "titulo": "6. Plazos de Inicio de Actividades y Término de Giro (Arts. 68 y 69 CT)",
        "formula": r"\text{Plazo Legal} = \text{Dentro de los 2 meses siguientes al mes del hecho}",
        "regla": "Si inicias o cesas actividades en octubre, el plazo vence el último día hábil de diciembre.",
    },
]

QUIZ_CATEDRA = [
    {
        "pregunta": "1. Una empresa constructora compra un automóvil station wagon para gerencia. ¿Puede usar ese IVA como Crédito Fiscal?",
        "opciones": [
            "Sí, siempre que tenga factura electrónica.",
            "No, el Art. 23 N° 4 del D.L. 825 excluye automóviles y station wagons del crédito fiscal.",
            "Sí, pero solo el 50% por proporcionalidad.",
        ],
        "correcta": 1,
        "explicacion": "Según el Art. 23 N° 4 del D.L. N° 825, el IVA en la compra de automóviles o station wagons no da derecho a crédito fiscal y se registra como IVA no recuperable (salvo giro habitual de venta/arriendo o autorización expresa).",
    },
    {
        "pregunta": "2. En el caso 'El Espejo Tributario (Constructora del Sur S.A.)', ¿cuál es el efecto de incorporar 3 facturas falsas por $50.000.000 netos ($9.500.000 de IVA)?",
        "opciones": [
            "Solo se paga una multa administrativa de 1 UTM.",
            "Se restituye el IVA Crédito Fiscal ($9.500.000), se rechaza el gasto en Renta y se configura delito tributario del Art. 97 N° 4 CT.",
            "Se compensa contra el remanente de UTM sin sanción penal.",
        ],
        "correcta": 1,
        "explicacion": "El uso malicioso de facturas falsas gatilla restitución del IVA indebido, rechazo del gasto en Renta y delito tributario del Art. 97 N° 4 CT (multa de 50% a 400% + presidio).",
    },
    {
        "pregunta": "3. Si una boleta de ventas tiene un total bruto de $119.000, ¿cuál es su monto neto y su IVA?",
        "opciones": [
            "Neto $96.390 e IVA $22.610.",
            "Neto $100.000 e IVA $19.000.",
            "Neto $100.000 e IVA $22.610.",
        ],
        "correcta": 1,
        "explicacion": "Neto = $119.000 / 1,19 = $100.000; IVA = $119.000 - $100.000 = $19.000.",
    },
    {
        "pregunta": "4. Desde la Ley N° 21.420 (enero 2023), un servicio de consultoría prestado por una SpA (sociedad de capital) está:",
        "opciones": [
            "Exento de IVA por ser servicio profesional.",
            "Afecto a IVA (19%), salvo exención expresa de los Arts. 12 o 13 de la LIVS.",
            "Afecto solo a retención de honorarios.",
        ],
        "correcta": 1,
        "explicacion": "La Ley N° 21.420 gravó con IVA todos los servicios prestados por sociedades de capital; solo las Sociedades de Profesionales registradas y exenciones legales mantienen la exención.",
    },
]

# ==============================================================================
# BARRA LATERAL Y NAVEGACION
# ==============================================================================
st.sidebar.title("Gestión Tributaria 2026")
st.sidebar.markdown("**Universidad de Los Lagos**  \nIngeniería Comercial | Semestre X  \nDocente: Richard Arnoldo Villanueva Soto")
st.sidebar.divider()

modulo_trib = st.sidebar.radio(
    "Módulos del Sistema Tributario:",
    [
        "1. Institucionalidad, Ciclo de Vida y Derechos (CT)",
        "2. Clasificador y Simulador de Rentas (1ª y 2ª Cat. UTM)",
        "3. Simulador IVA, Proporcionalidad, Art. 23 N°4 y Excel F29",
        "4. Analítica PGCT 2026: Fiscalización, Brechas y Riesgo SII",
        "5. Infracciones y Delitos (Art. 97 CT y Caso Espejo Tributario)",
        "6. Entrenamiento Mecánico (Modo Ciego) y Quiz de Cátedra",
    ],
)

# ==============================================================================
# MODULO 1: INSTITUCIONALIDAD, CICLO DE VIDA Y DERECHOS
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

        st.markdown("**Verificador Rápido de Plazos Legales (Inicio y Término de Giro - Arts. 68 y 69 CT)**")
        meses_lista = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
        ]
        mes_evento = st.selectbox("Mes en que inició operaciones o cesó actividades:", meses_lista, index=9)
        mes_limite = meses_lista[(meses_lista.index(mes_evento) + 2) % 12]
        st.success(f"Si el hecho ocurrió en **{mes_evento}**, el plazo legal vence el **último día hábil de {mes_limite}** (dentro de los 2 meses siguientes).")

    with t3:
        c_der, c_deb = st.columns([3, 2])
        with c_der:
            st.subheader("Catálogo de los 20 Derechos del Contribuyente (Art. 8 bis CT)")
            busqueda_der = st.text_input("Filtrar derecho por palabra clave (ej. fiscalización, buena fe, devolución):", "")
            for d in [x for x in DERECHOS_CONTRIBUYENTE_8BIS if busqueda_der.lower() in x.lower()]:
                st.markdown(f"- {d}")
            st.caption("**Art. 8 ter y 8 quáter:** Derecho a autorización de DTE necesarios para el giro y publicación en MiSII de cualquier restricción.")
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
# MODULO 2: CLASIFICADOR Y SIMULADOR DE RENTAS (1A Y 2A CATEGORIA EN UTM)
# ==============================================================================
elif modulo_trib.startswith("2."):
    st.markdown("<div class='sec-header'>2. CLASIFICACIÓN TRIBUTARIA DE LAS RENTAS Y SIMULADOR DE IMPUESTO ÚNICO (UTM)</div>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.subheader("Comparador: Empresario Individual vs. Persona Jurídica")
        df_figuras = pd.DataFrame({
            "Atributo Legal y Tributario": [
                "Conformación", "Constitución Legal", "Rol Único Tributario (RUT)",
                "Responsabilidad Patrimonial", "Exigencia de Capital Inicial", "Figuras Típicas",
            ],
            "Persona Natural (Empresario Individual)": [
                "1 sola persona natural", "No requiere escritura social", "Usa el mismo RUN personal",
                "Ilimitada (responde con patrimonio personal)", "No requiere acreditar capital mínimo",
                "Empresa Individual / Microempresa Familiar (MEF)",
            ],
            "Persona Jurídica (Sociedad / EIRL)": [
                "1 o más personas naturales o jurídicas", "Requiere escritura e inscripción legal",
                "RUT propio e independiente de los socios", "Limitada al capital o bienes de la empresa",
                "Requiere aporte de capital en dinero o bienes", "SpA, Ltda., S.A., EIRL, Soc. Colectiva",
            ],
        })
        st.dataframe(df_figuras, use_container_width=True, hide_index=True)

    with col_r2:
        st.subheader("Simulador de Rentas: Primera vs. Segunda Categoría")
        tipo_renta = st.selectbox(
            "Selecciona el origen de la renta a evaluar:",
            [
                "1ª Categoría: Industria, Comercio, Minería o Servicios de Capital",
                "2ª Categoría Independiente: Boleta de Honorarios Electrónica (Art. 42 N°2 LIR)",
                "2ª Categoría Dependiente: Sueldo Tributable Mensual (Impuesto Único en UTM)",
            ],
        )
        monto_bruto = st.number_input("Monto Base / Renta Tributable del Período ($ CLP):", min_value=0, value=2500000, step=100000)

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
        elif "Honorarios" in tipo_renta:
            tasa_ret = st.slider("Tasa de Retención Boleta de Honorarios (%):", min_value=10.0, max_value=17.0, value=15.25, step=0.75)
            retencion = monto_bruto * (tasa_ret / 100.0)
            liquido = monto_bruto - retencion
            st.metric("Monto Líquido a Recibir", f"${liquido:,.0f} CLP", f"Retención SII: ${retencion:,.0f} ({tasa_ret}%)")
        else:
            utm_iusc = st.number_input("Valor UTM del Mes ($ CLP):", min_value=1000, value=67500, step=500, key="utm_iusc")
            res_iu = m_sii.calcular_impuesto_unico_2da_cat(monto_bruto, utm_iusc)
            m1, m2, m3 = st.columns(3)
            m1.metric("Renta en UTM", f"{res_iu['renta_utm']:.2f} UTM", res_iu["tramo"])
            m2.metric("Impuesto Único a Retener", f"${res_iu['impuesto_clp']:,.0f}", f"Tasa efectiva: {res_iu['tasa_efectiva_pct']:.2f}%")
            m3.metric("Sueldo Después de Impuesto", f"${res_iu['liquido_estimado_clp']:,.0f}", f"Factor: {res_iu['factor']*100:.1f}%")
            with st.expander("Ver Tabla Oficial de Tramos Impuesto Único (UTM y CLP)"):
                st.dataframe(m_sii.tabla_tramos_iusc_df(utm_iusc), use_container_width=True, hide_index=True)

# ==============================================================================
# MODULO 3: SIMULADOR IVA, PROPORCIONALIDAD ACUMULADA, ART. 23 N°4 Y EXCEL F29
# ==============================================================================
elif modulo_trib.startswith("3."):
    st.markdown("<div class='sec-header'>3. IMPUESTO AL VALOR AGREGADO (DL N° 825): F29, PROPORCIONALIDAD ACUMULADA, ART. 23 N°4 Y EXCEL</div>", unsafe_allow_html=True)

    iva_tab1, iva_tab2, iva_tab3, iva_tab4 = st.tabs([
        "I. Liquidación F29 y Exportador Excel",
        "II. Exclusión de Automóviles (Art. 23 N° 4)",
        "III. Hecho Gravado Servicios (Ley 21.420)",
        "IV. Matriz Auditoría RCV - F29",
    ])

    with iva_tab1:
        st.subheader("Simulador de Liquidación Mensual de IVA (Formulario 29)")
        c_vta, c_cmp, c_res = st.columns(3)

        with c_vta:
            st.markdown("**1. Operaciones de Venta y Débito Fiscal**")
            ventas_afectas_neto = st.number_input("Ventas Afectas Netas del Mes ($):", min_value=0, value=10000000, step=500000)
            ventas_exentas = st.number_input("Ventas Exentas / No Gravadas del Mes ($):", min_value=0, value=2000000, step=500000)
            notas_debito_neto = st.number_input("(+) Notas de Débito Emitidas Netas ($):", min_value=0, value=0, step=100000)
            notas_credito_neto = st.number_input("(-) Notas de Crédito Emitidas Netas ($):", min_value=0, value=0, step=100000)

            usar_acum = st.checkbox("Usar ventas acumuladas anuales para proporcionalidad (Regla D.L. 825)", value=False)
            base_debito = max(0.0, ventas_afectas_neto + notas_debito_neto - notas_credito_neto)
            debito_fiscal = base_debito * 0.19

            if usar_acum:
                acum_afectas_prev = st.number_input("Ventas Afectas Acumuladas Meses Anteriores ($):", min_value=0, value=30000000, step=1000000)
                acum_exentas_prev = st.number_input("Ventas Exentas Acumuladas Meses Anteriores ($):", min_value=0, value=5000000, step=500000)
                acum_afectas = acum_afectas_prev + base_debito
                acum_exentas = acum_exentas_prev + ventas_exentas
            else:
                acum_afectas = base_debito
                acum_exentas = ventas_exentas

            total_prop = acum_afectas + acum_exentas
            prop_afecta = (acum_afectas / total_prop * 100.0) if total_prop > 0 else 100.0

        with c_cmp:
            st.markdown("**2. Adquisiciones y Crédito Fiscal (RCV)**")
            compras_giro_neto = st.number_input("Compras Afectas Exclusivas Giro Afecto ($):", min_value=0, value=6000000, step=500000)
            compras_uso_comun_neto = st.number_input("Compras Afectas de Uso Común ($):", min_value=0, value=3000000, step=500000)
            compras_exentas_vinculo = st.number_input("Compras Giro Exento / Automóviles Art. 23 N°4 ($):", min_value=0, value=500000, step=100000)
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
            st.caption(f"IVA no recuperable (pasa a costo/gasto): **${iva_no_recuperable:,.0f} CLP**.")

            datos_export = {
                "ventas_afectas_neto": ventas_afectas_neto,
                "ventas_exentas": ventas_exentas,
                "notas_debito_neto": notas_debito_neto,
                "notas_credito_neto": notas_credito_neto,
                "acum_afectas": acum_afectas,
                "acum_exentas": acum_exentas,
                "compras_giro_neto": compras_giro_neto,
                "compras_uso_comun_neto": compras_uso_comun_neto,
                "compras_exentas_vinculo": compras_exentas_vinculo,
                "remanente_utm_ant": remanente_utm_ant,
                "valor_utm": valor_utm,
            }
            excel_bytes = m_sii.exportar_libros_y_f29_excel(datos_export)
            st.download_button(
                label="Descargar Libros y F29 en Excel (.xlsx con Fórmulas Vivas)",
                data=excel_bytes,
                file_name="Libros_RCV_y_F29_Formulas_Vivas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        st.divider()
        st.markdown("**Conversor Rápido Precio Neto / Precio Bruto con IVA (19%)**")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            monto_conv = st.number_input("Ingresa monto a convertir ($):", min_value=0, value=1190000, step=10000)
        with col_c2:
            modo_conv = st.radio("Tipo de monto ingresado:", ["Precio Total con IVA incluido (÷ 1,19)", "Precio Neto sin IVA (× 1,19)"])
        if modo_conv.startswith("Precio Total"):
            neto_calc = monto_conv / 1.19
            st.info(f"**Neto:** ${neto_calc:,.0f} | **IVA (19%):** ${monto_conv - neto_calc:,.0f} | **Total Bruto:** ${monto_conv:,.0f}")
        else:
            iva_calc = monto_conv * 0.19
            st.info(f"**Neto:** ${monto_conv:,.0f} | **IVA (19%):** ${iva_calc:,.0f} | **Total Bruto:** ${monto_conv + iva_calc:,.0f}")

    with iva_tab2:
        st.subheader("Simulador Art. 23 N° 4 D.L. 825: Exclusión de Automóviles vs. Vehículos de Trabajo")
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            tipo_veh = st.selectbox(
                "Tipo de bien adquirido por la empresa:",
                [
                    "Automóvil / Station Wagon (uso gerencial o comercial)",
                    "Furgón de reparto cerrado (vehículo de carga)",
                    "Grúa horquilla / Maquinaria industrial",
                    "Camioneta de trabajo adaptada exclusivamente a carga",
                ],
            )
            valor_neto_veh = st.number_input("Valor Neto Factura del Vehículo ($ CLP):", min_value=0, value=18000000, step=500000)
        with c_v2:
            iva_veh = valor_neto_veh * 0.19
            es_excluido = tipo_veh.startswith("Automóvil")
            if es_excluido:
                st.error("**NO da derecho a Crédito Fiscal (Art. 23 N° 4 D.L. 825)**")
                st.metric("IVA No Recuperable (Pasa a Costo del Activo)", f"${iva_veh:,.0f} CLP", "0% Crédito Fiscal")
                st.caption("Base de activación / costo total: " + f"${valor_neto_veh + iva_veh:,.0f} CLP.")
            else:
                st.success("**SÍ da derecho a Crédito Fiscal (100% vinculado al giro afecto)**")
                st.metric("IVA Crédito Fiscal Aprovechable", f"${iva_veh:,.0f} CLP", "100% Crédito Fiscal")
                st.caption("Valor neto activable: " + f"${valor_neto_veh:,.0f} CLP.")

    with iva_tab3:
        st.subheader("Árbol de Decisión: Tributación de Servicios desde Ley N° 21.420 (Arts. 2, 12 y 13 LIVS)")
        p1 = st.checkbox("1. ¿Existe una acción o prestación remunerada?", value=True)
        p2 = st.selectbox("2. ¿Quién presta el servicio?", [
            "Sociedad de Capital (SpA, S.A., Ltda. comercial/consultora)",
            "Sociedad de Profesionales registrada en el SII",
            "Persona Natural independiente (Boleta de Honorarios)",
            "Establecimiento de Educación / Salud / Transporte de Pasajeros (Arts. 12 y 13 LIVS)",
        ])
        if not p1:
            st.warning("Operación **No Gravada / No Afecta**.")
        elif "Sociedad de Capital" in p2:
            st.error("Operación **Afecta a IVA (19%)** desde el 1 de enero de 2023 (Ley N° 21.420).")
        else:
            st.success("Operación **Exenta de IVA** (recordar proporcionalidad sobre compras de uso común).")

    with iva_tab4:
        st.subheader("Matriz de Control de Auditoría Tributaria y Plazos F29")
        df_aud_iva = pd.DataFrame([
            {"Etapa": "Ventas", "Pregunta de Control": "¿Todas las ventas afectas fueron documentadas?", "Evidencia": "DTE, RCV, vouchers POS, bancos", "Riesgo": "Débito fiscal omitido"},
            {"Etapa": "Compras", "Pregunta de Control": "¿El crédito fiscal cumple Arts. 23 y 25 LIVS?", "Evidencia": "RCV, acuse de recibo, vínculo al giro", "Riesgo": "Crédito fiscal improcedente"},
            {"Etapa": "Devengo", "Pregunta de Control": "¿Se reconoció en el mes legalmente correcto?", "Evidencia": "Fecha emisión DTE, guías de despacho", "Riesgo": "Diferencias mensuales y multas"},
            {"Etapa": "Notas NC/ND", "Pregunta de Control": "¿Están referenciadas y dentro de plazo?", "Evidencia": "Notas de Crédito/Débito y DTE original", "Riesgo": "IVA sobre o subdeclarado"},
            {"Etapa": "Formulario 29", "Pregunta de Control": "¿Cuadra RCV con libro mayor contable y F29?", "Evidencia": "F29, RCV, balance y mayor contable", "Riesgo": "Observaciones SII y rectificatorias"},
        ])
        st.dataframe(df_aud_iva, use_container_width=True, hide_index=True)

# ==============================================================================
# MODULO 4: ANALITICA PGCT 2026
# ==============================================================================
elif modulo_trib.startswith("4."):
    st.markdown("<div class='sec-header'>4. PLAN DE GESTIÓN DE CUMPLIMIENTO TRIBUTARIO (PGCT 2026 - LEY N° 21.713)</div>", unsafe_allow_html=True)

    pg1, pg2, pg3 = st.tabs([
        "I. Fiscalización y Recaudación por Segmento",
        "II. Brechas de Evasión IVA y Control de Fraude",
        "III. Capacidades SII, Dotación y Formación PFI 2026",
    ])

    with pg1:
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
        k1.metric("Total Contribuyentes", "6.048.466", "+15,4% Inicios 1ª Cat.")
        k2.metric("Recaudación Total", "$55.436.217 MM", "67% Grandes Empresas")
        k3.metric("Auditorías y Revisiones", "20.382", "5.891 Aud. + 14.491 Rev.")
        k4.metric("Autocorrección en Línea", "75,6%", "248.868 contribuyentes")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.plotly_chart(px.pie(df_fisc, values="Recaudación_MM_CLP", names="Segmento", hole=0.4, title="Participación en Recaudación por Segmento"), use_container_width=True)
        with col_f2:
            st.plotly_chart(px.bar(df_fisc, x="Segmento", y=["%_Horas_Fisc", "%_Recaudación"], barmode="group", title="Focalización: % Horas vs. % Recaudación"), use_container_width=True)
        st.dataframe(df_fisc, use_container_width=True, hide_index=True)

    with pg2:
        df_eva = pd.DataFrame({
            "País / Bloque": ["Perú", "Promedio América Latina", "Colombia", "Chile (2023)", "Italia", "Francia", "España", "Austria"],
            "Tasa_Evasión_IVA (%)": [32.2, 27.6, 23.6, 18.2, 14.7, 9.7, 7.1, 3.9],
        })
        st.plotly_chart(px.bar(df_eva, x="Tasa_Evasión_IVA (%)", y="País / Bloque", orientation="h", color="Tasa_Evasión_IVA (%)", color_continuous_scale="RdYlGn_r", title="Tasa de Evasión de IVA Comparada (%)"), use_container_width=True)
        c_d1, c_d2, c_d3, c_d4 = st.columns(4)
        c_d1.metric("Nuevos Emisores Agresivos", "18.060", "+30,8%")
        c_d2.metric("Crédito Fiscal Indebido Evitado", "$189.400 MM", "81.720 receptores")
        c_d3.metric("Querellas y Denuncias 2025", "227 causas", "$158.000 MM perjuicio")
        c_d4.metric("Efectividad Sanción Penal", "80,5%", "136 de 169 causas")

    with pg3:
        df_dot = pd.DataFrame({
            "Escalafón": ["Fiscalizador Tributario", "Profesional", "Administrativo", "Fiscalizador Tasador", "Técnico Fiscalizador", "Directivo", "Auxiliar", "Técnico Informática", "Técnico Avaluaciones"],
            "Funcionarios": [1774, 1354, 784, 329, 220, 218, 144, 68, 22],
        })
        df_pfi = pd.DataFrame({
            "Foco Formativo PFI 2026": ["Gestión de Cumplimiento", "Base Contable y Tributaria", "Liderazgo y Equipos", "Procedimientos Transversales", "Análisis de Datos y Digital"],
            "Cupos": [5093, 1408, 1281, 923, 888],
        })
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.plotly_chart(px.bar(df_dot, x="Escalafón", y="Funcionarios", title="Dotación SII por Escalafón (4.913 funcionarios)"), use_container_width=True)
        with col_p2:
            st.plotly_chart(px.pie(df_pfi, values="Cupos", names="Foco Formativo PFI 2026", hole=0.4, title="Distribución de los 9.593 Cupos PFI 2026"), use_container_width=True)

# ==============================================================================
# MODULO 5: INFRACCIONES Y DELITOS (ART. 97 CT Y CASO EL ESPEJO TRIBUTARIO)
# ==============================================================================
elif modulo_trib.startswith("5."):
    st.markdown("<div class='sec-header'>5. INFRACCIONES, SANCIONES Y DELITOS TRIBUTARIOS (ART. 97 CÓDIGO TRIBUTARIO)</div>", unsafe_allow_html=True)

    tab_a97, tab_espejo = st.tabs([
        "I. Calculadora de Sanciones Art. 97 CT",
        "II. Caso de Cátedra: El Espejo Tributario (Constructora del Sur S.A.)",
    ])

    with tab_a97:
        st.subheader("Simulador de Multas e Infracciones del Artículo 97 (D.L. N° 830)")
        c_s1, c_s2 = st.columns(2)
        with c_s1:
            numeral = st.selectbox(
                "Selecciona infracción / delito a simular:",
                [
                    "Art. 97 N° 4 (Inc. 2°): Facturas falsas / Aumento indebido de crédito fiscal",
                    "Art. 97 N° 10: No emisión de boletas o facturas",
                    "Art. 97 N° 11: Retardo en enterar impuestos de retención o recargo (IVA)",
                    "Art. 97 N° 2: Retardo u omisión de declaraciones con impuesto",
                ],
            )
            tributo_base = st.number_input("Monto del Tributo Eludido / Operación ($ CLP):", min_value=0, value=9500000, step=500000)
            meses_atraso = st.slider("Meses de atraso (aplica a N° 2 y N° 11):", 1, 24, 3)

        with c_s2:
            if "N° 4" in numeral:
                st.error("**Delito Tributario Penal (Art. 97 N° 4 CT + Ley N° 20.393)**")
                m_min, m_max = tributo_base * 0.50, tributo_base * 4.00
                st.metric("Rango de Multa Legal (50% a 400%)", f"${m_min:,.0f} a ${m_max:,.0f} CLP")
                st.caption("Además conlleva pena corporal de presidio y restitución íntegra del tributo reajustado con intereses.")
            elif "N° 10" in numeral:
                st.warning("**Infracción Administrativa Grave (Art. 97 N° 10 CT)**")
                m_min, m_max = tributo_base * 0.50, tributo_base * 5.00
                st.metric("Multa (50% a 500% del monto de la operación)", f"${m_min:,.0f} a ${m_max:,.0f} CLP")
                st.caption("Mínimo 2 UTM y máximo 40 UTA, más clausura del establecimiento hasta por 20 días.")
            elif "N° 11" in numeral:
                pct = min(30.0, 10.0 + max(0, meses_atraso - 5) * 2.0)
                st.warning("**Retardo en Impuestos de Recargo / Retención (Art. 97 N° 11 CT)**")
                st.metric(f"Multa Aplicable ({pct:.0f}%)", f"${tributo_base * (pct / 100.0):,.0f} CLP")
                st.caption("10% base + 2% por cada mes o fracción adicional desde el 6° mes, con tope de 30% (60% si es detectado en fiscalización).")
            else:
                pct = min(30.0, 10.0 + max(0, meses_atraso - 5) * 2.0)
                st.info("**Retardo en Declaración con Impuesto (Art. 97 N° 2 CT)**")
                st.metric(f"Multa Aplicable ({pct:.0f}%)", f"${tributo_base * (pct / 100.0):,.0f} CLP")
                st.caption("10% durante los primeros 5 meses + 2% adicional por mes, tope 30%.")

    with tab_espejo:
        st.subheader("Caso Oficial: El Espejo Tributario — Constructora del Sur S.A.")
        st.markdown(
            "Simulación del impacto tributario y penal al incorporar **3 facturas ideológicamente falsas** "
            "para rebajar IVA y aumentar gastos en Renta."
        )
        c_e1, c_e2, c_e3 = st.columns(3)
        neto_falso = c_e1.number_input("Monto Neto Facturas Falsas ($ CLP):", min_value=0, value=50000000, step=1000000)
        tasa_renta_emp = c_e2.selectbox("Tasa Renta / Art. 21 LIR aplicable (%):", [25.0, 27.0, 40.0], index=2)
        pct_multa_penal = c_e3.slider("Escenario Multa Art. 97 N° 4 (% sobre IVA eludido):", 50, 400, 100, 50)

        iva_indebido = neto_falso * 0.19
        imp_gasto_rech = neto_falso * (tasa_renta_emp / 100.0)
        multa_97_4 = iva_indebido * (pct_multa_penal / 100.0)
        costo_total_fraude = iva_indebido + imp_gasto_rech + multa_97_4

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("1. Restitución IVA Crédito", f"${iva_indebido:,.0f}", "19% sobre neto falso")
        k2.metric("2. Impacto Renta / Art. 21", f"${imp_gasto_rech:,.0f}", f"Tasa {tasa_renta_emp:.0f}%")
        k3.metric("3. Multa Art. 97 N° 4", f"${multa_97_4:,.0f}", f"{pct_multa_penal}% del IVA")
        k4.metric("Contingencia Total Estimada", f"${costo_total_fraude:,.0f}", "Sin intereses ni reajustes")

# ==============================================================================
# MODULO 6: ENTRENAMIENTO MECANICO (MODO CIEGO) Y QUIZ DE CATEDRA
# ==============================================================================
elif modulo_trib.startswith("6."):
    st.markdown("<div class='sec-header'>6. ENTRENAMIENTO MECÁNICO (MODO CIEGO) Y CONTROL DE CÁTEDRA</div>", unsafe_allow_html=True)

    tab_mc, tab_qz = st.tabs([
        "I. Formulario Mecánico (Modo Ciego)",
        "II. Control Rápido de Cátedra (4 Preguntas)",
    ])

    with tab_mc:
        modo_ciego = st.toggle("Activar Modo Ciego (oculta fórmulas y reglas para comprobar contra tu cuaderno)", value=False)
        for item in FORMULAS_MODO_CIEGO:
            with st.container(border=True):
                st.markdown(f"**{item['titulo']}**")
                if modo_ciego:
                    with st.expander("Mostrar fórmula y regla para comprobar"):
                        st.latex(item["formula"])
                        st.write(item["regla"])
                else:
                    st.latex(item["formula"])
                    st.caption(item["regla"])

    with tab_qz:
        puntaje = 0
        for idx, q in enumerate(QUIZ_CATEDRA):
            st.markdown(f"**{q['pregunta']}**")
            sel = st.radio("Selecciona una alternativa:", q["opciones"], index=None, key=f"qz_trib_{idx}")
            if sel is not None:
                if q["opciones"].index(sel) == q["correcta"]:
                    puntaje += 1
                    st.success(f"Correcto. {q['explicacion']}")
                else:
                    st.error(f"Incorrecto. {q['explicacion']}")
            st.divider()
        st.metric("Resultado Actual del Control", f"{puntaje} / {len(QUIZ_CATEDRA)}")
