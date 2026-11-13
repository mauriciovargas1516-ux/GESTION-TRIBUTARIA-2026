# Suite de Gestión Tributaria para la Toma de Decisiones 2026 — ULagos

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)
[![Lanzar Suite Tributaria en Streamlit](https://img.shields.io/badge/🚀_ABRIR_SUITE_TRIBUTARIA_EN_STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/mauriciovargas1516-ux/GESTION-TRIBUTARIA-2026)

Plataforma interactiva desarrollada en **Python y Streamlit** para el análisis normativo, simulación impositiva (DL N° 825 / Ley sobre Impuesto a la Renta) y control de cumplimiento tributario en el marco de la asignatura **Gestión Tributaria para la Toma de Decisiones** de la carrera de Ingeniería Comercial en la Universidad de Los Lagos (Docente: Richard Arnoldo Villanueva Soto).

**Acceso directo a la aplicación web en vivo:**  
 **[https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)**

---

## 1. Módulos Integrados en el Sistema

### Módulo 1: Institucionalidad, Ciclo de Vida y Derechos del Contribuyente (Código Tributario)
* **Ecosistema de Administración Tributaria:** Estructura funcional del Ministerio de Hacienda, Servicio de Impuestos Internos (SII), Tesorería General de la República (TGR) y Servicio Nacional de Aduanas (SNA), junto con la línea de tiempo normativa desde 1902 hasta la Ley N° 21.713.
* **Las 5 Etapas del Ciclo de Vida:** Matriz operativa desde Obtención de RUT e Inicio de Actividades hasta Término de Giro, con verificador automático de plazos legales (artículos 68 y 69 del Código Tributario).
* **Derechos y Deberes Legales:** Buscador interactivo de los 20 derechos del contribuyente establecidos en el artículo 8 bis (más artículos 8 ter y 8 quáter) y los 9 deberes tributarios.

### Módulo 2: Clasificador y Simulador de Rentas (Primera vs. Segunda Categoría — LIR)
* **Estructura Jurídica y Patrimonial:** Comparador técnico entre Persona Natural (Empresario Individual / Microempresa Familiar) y Persona Jurídica (SpA, Ltda., S.A., EIRL).
* **Simulador de Impuesto a la Renta:** Cálculo de Impuesto de Primera Categoría sobre Renta Líquida Imponible (Regímenes Pro Pyme y Semi Integrado) y simulador de retenciones en Boletas de Honorarios Electrónicas (artículo 42 N° 2 de la LIR).

### Módulo 3: Simulador de IVA, Proporcionalidad y Auditoría F29 (DL N° 825 — LIVS)
* **Liquidación Mensual de IVA:** Determinación de Débito Fiscal, Crédito Fiscal directo y cálculo automático del coeficiente de proporcionalidad para adquisiciones de uso común frente a ventas afectas y exentas.
* **Remanente en UTM y Conversor:** Transformación automática del saldo a favor de crédito fiscal a Unidades Tributarias Mensuales (UTM) y conversor rápido Neto a Bruto (19%).
* **Tributación de Servicios y Auditoría RCV-F29:** Calificador de hecho gravado en servicios bajo la Ley N° 21.420 (Sociedades de Capital vs. Sociedades de Profesionales y exenciones de los artículos 12 y 13 de la LIVS) y matriz de control de auditoría para el Formulario 29.

### Módulo 4: Analítica del Plan de Gestión de Cumplimiento Tributario (PGCT 2026 — SII)
* **Fiscalización y Recaudación por Segmento:** Panel interactivo del Modelo de Gestión de Cumplimiento Tributario (MGCT) desglosado en Grandes, Medianas, Pequeñas, Microempresas, Altos Patrimonios y Personas Naturales.
* **Brechas de Evasión y Delito Tributario:** Comparativa internacional de tasas de evasión de IVA, control de emisores agresivos de facturas falsas y persecución penal del crimen organizado.
* **Capacidades Institucionales:** Distribución de la dotación del SII por escalafón y cobertura del Plan de Formación Institucional (PFI 2026).

---

## 2. Estructura del Repositorio

| Archivo | Descripción Técnica |
| :--- | :--- |
| **app.py** | Motor principal en Streamlit con los 4 módulos tributarios, simuladores interactivos y gráficos en Plotly. |
| **requirements.txt** | Dependencias de Python necesarias para el despliegue en Streamlit Cloud y ejecución local. |

---

## 3. Instalación y Ejecución Local

```bash
git clone [https://github.com/mauriciovargas1516-ux/GESTION-TRIBUTARIA-2026.git](https://github.com/mauriciovargas1516-ux/GESTION-TRIBUTARIA-2026.git)
cd GESTION-TRIBUTARIA-2026
pip install -r requirements.txt
streamlit run app.py
