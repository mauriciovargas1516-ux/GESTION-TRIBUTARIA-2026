
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA - GESTIÓN TRIBUTARIA 2026 (PARTE 1 DE 2)
# ==============================================================================
st.set_page_config(
    page_title="Gestión Tributaria para la Toma de Decisiones 2026 - ULagos",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
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
st.sidebar.title("⚖️ Gestión Tributaria 2026")
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

st.title("⚖️ Suite de Gestión Tributaria para la Toma de Decisiones 2026")
st.caption("Motor Normativo, Simulador de Impuestos (DL 825 / LIR) y Analítica de Cumplimiento PGCT 2026 | ULagos")

# ==============================================================================
# MÓDULO 1: INSTITUCIONALIDAD, CICLO DE VIDA Y DERECHOS DEL CONTRIBUYENTE
# ==============================================================================
if modulo_trib.startswith("1."):
    st.header("1. Educación Fiscal, Administración Tributaria y Ciclo de Vida del Contribuyente")

    t1, t2, t3 = st.tabs([
        "🏛️ Ecosistema Hacienda y Evolución SII",
        "🔄 Las 5 Etapas del Ciclo de Vida",
        "🛡️ Derechos (Art. 8 bis / ter / quáter) y Deberes",
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
        mes_evento = st.selectbox("Mes en que inició operaciones o cesó actividades:", [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ], index=9)
        meses_lista = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        idx_m = meses_lista.index(mes_evento)
        mes_limite = meses_lista[(idx_m + 2) % 12]
        st.success(f"📌 Si el hecho ocurrió en **{mes_evento}**, el plazo legal vence el **último día hábil de {mes_limite}** (dentro de los 2 meses siguientes).")

    with t3:
        c_der, c_deb = st.columns([3, 2])
        with c_der:
            st.subheader("Catálogo de los 20 Derechos del Contribuyente (Art. 8 bis CT)")
            busqueda_der = st.text_input("🔍 Filtrar derecho por palabra clave (ej. fiscalización, buena fe, devolución):", "")
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
    st.header("2. Clasificación Tributaria de las Rentas y Estructura Jurídica")

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
            tasa_idpc = st.radio("Régimen de Primera Categoría:", [12.5, 25.0, 27.0], index=1, format_func=lambda x: f"{x}% ({'Pro Pyme Transitorio' if x==12.5 else 'Pro Pyme General 14D3' if x==25.0 else 'Semi Integrado 14A'})", horizontal=True)
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
