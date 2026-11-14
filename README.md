# Suite de Gestión Tributaria para la Toma de Decisiones 2026 — ULagos

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)
[![Lanzar Suite Tributaria en Streamlit](https://img.shields.io/badge/ABRIR_SUITE_TRIBUTARIA_EN_STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/mauriciovargas1516-ux/GESTION-TRIBUTARIA-2026)

Plataforma interactiva desarrollada en **Python y Streamlit** para el análisis normativo, simulación impositiva (**DL N° 825 / Ley sobre Impuesto a la Renta / Código Tributario**) y control de cumplimiento tributario en el marco de la asignatura **Gestión Tributaria para la Toma de Decisiones** (Ingeniería Comercial, Universidad de Los Lagos — Docente: Richard Arnoldo Villanueva Soto).

**Acceso directo a la aplicación web en vivo:**  
[https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/](https://gestion-tributaria-2026-avecwdhabftj7rjnx5knmb.streamlit.app/)

---

## Guía Rápida de Uso

1. **Seleccionar el Módulo en el Panel Lateral:** Navega entre los 4 bloques normativos y cuantitativos (Código Tributario, Rentas LIR, Simulador IVA F29 y Analítica PGCT 2026).
2. **Ingresar Montos o Consultas Normativas:** Modifica en vivo las ventas afectas, ventas exentas, compras de uso común, valor de la UTM o rentas brutas para obtener el cálculo inmediato del impuesto o retención.
3. **Auditar Plazos y Criterios SII:** Utiliza el verificador automático de plazos legales (Arts. 68 y 69 CT) y el árbol de decisión de IVA en servicios (Ley N° 21.420).

---

## Impacto Cuantitativo y Multiplicadores de Velocidad (Motor Tributario vs. Cálculo Manual)

| Tarea de Cumplimiento o Simulación Tributaria | Volumen Normativo / Operativo | Tiempo Manual (Planillas / Leyes) | Tiempo Cloud | Horas Ahorradas | % Mejora (Multiplicador) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Liquidación Mensual IVA F29 + Cálculo de Proporcionalidad y Remanente en UTM** | Ventas afectas/exentas + RCV uso común + conversión UTM | 2,5 horas | **0,02 hrs** (1 min) | 2,48 hrs/caso | **99,2% (125,0x más rápido)** |
| **2. Simulación Comparada de Rentas (1ª Categoría 14D3 / 14A vs. 2ª Categoría)** | Regímenes Pro Pyme (12,5% / 25%), Semi Integrado (27%) y Honorarios | 1,8 horas | **0,01 hrs** (30 seg) | 1,79 hrs/caso | **99,4% (180,0x más rápido)** |
| **3. Calificación de Hecho Gravado en Servicios (Ley 21.420) y Auditoría RCV-F29** | Árbol Arts. 2, 12 y 13 LIVS + 5 controles de devengo y notas NC/ND | 2,2 horas | **0,02 hrs** (1 min) | 2,18 hrs/auditoría | **99,1% (110,0x más rápido)** |
| **4. Búsqueda Normativa en Código Tributario (Arts. 8 bis/ter/quáter, 68 y 69)** | 20 Derechos, 9 Deberes, 11 hitos históricos y 5 etapas ciclo de vida | 1,5 horas | **0,01 hrs** (20 seg) | 1,49 hrs/consulta | **99,3% (150,0x más rápido)** |
| **5. Cruce Estadístico del Plan de Gestión de Cumplimiento Tributario (PGCT 2026)** | 6.048.466 contribuyentes, 6 segmentos SII y tasas de evasión OCDE/Latam | 3,5 horas | **0,02 hrs** (1 min) | 3,48 hrs/análisis | **99,4% (175,0x más rápido)** |
| **TOTAL CICLO DE AUDITORÍA Y SIMULACIÓN IMPOSITIVA** | **CT + LIR + DL 825 (LIVS) + PGCT 2026 SII** | **11,5 horas** | **0,08 hrs (5 min)** | **11,42 horas** | **99,3% (143,8x más rápido)** |

---

## Arquitectura de los 4 Módulos del Sistema

### Módulo 1: Institucionalidad, Ciclo de Vida y Derechos del Contribuyente (Código Tributario)
* **Ecosistema de Administración Tributaria:** Estructura funcional del Ministerio de Hacienda, Servicio de Impuestos Internos (SII), Tesorería General de la República (TGR) y Servicio Nacional de Aduanas (SNA), junto con la línea de tiempo normativa desde 1902 hasta la Ley N° 21.713.
* **Las 5 Etapas del Ciclo de Vida:** Matriz operativa desde Obtención de RUT e Inicio de Actividades hasta Término de Giro, con verificador automático de plazos legales (artículos 68 y 69 del Código Tributario).
* **Derechos y Deberes Legales:** Buscador interactivo por palabra clave de los 20 derechos del contribuyente establecidos en el artículo 8 bis (más artículos 8 ter y 8 quáter) y los 9 deberes tributarios.

### Módulo 2: Clasificador y Simulador de Rentas (Primera vs. Segunda Categoría — LIR)
* **Estructura Jurídica y Patrimonial:** Comparador técnico entre Persona Natural (Empresario Individual / Microempresa Familiar) y Persona Jurídica (SpA, Ltda., S.A., EIRL).
* **Simulador de Impuesto a la Renta:** Cálculo de Impuesto de Primera Categoría sobre Renta Líquida Imponible (Regímenes Pro Pyme Transitorio 12,5%, Pro Pyme General 25% y Semi Integrado 27%) y simulador de retenciones en Boletas de Honorarios Electrónicas (artículo 42 N° 2 de la LIR).

### Módulo 3: Simulador de IVA, Proporcionalidad y Auditoría F29 (DL N° 825 — LIVS)
* **Liquidación Mensual de IVA:** Determinación de Débito Fiscal, Crédito Fiscal directo y cálculo automático del coeficiente de proporcionalidad para adquisiciones de uso común frente a ventas afectas y exentas, aislando automáticamente el IVA no recuperable que pasa a costo/gasto.
* **Remanente en UTM y Conversor:** Transformación automática del saldo a favor de crédito fiscal a Unidades Tributarias Mensuales (UTM) y conversor bidireccional Neto $\leftrightarrow$ Bruto (19%).
* **Tributación de Servicios y Auditoría RCV-F29:** Calificador interactivo de hecho gravado en servicios bajo la Ley N° 21.420 (Sociedades de Capital vs. Sociedades de Profesionales y exenciones de los artículos 12 y 13 de la LIVS) y matriz de control de auditoría para el Formulario 29.

### Módulo 4: Analítica del Plan de Gestión de Cumplimiento Tributario (PGCT 2026 — SII)
* **Fiscalización y Recaudación por Segmento:** Panel interactivo del Modelo de Gestión de Cumplimiento Tributario (MGCT) sobre 6.048.466 contribuyentes desglosados en Grandes, Medianas, Pequeñas, Microempresas, Altos Patrimonios y Personas Naturales ($55,4 billones CLP de recaudación).
* **Brechas de Evasión y Delito Tributario:** Comparativa internacional de tasas de evasión de IVA (Chile 18,2% vs. América Latina y Europa), control de 18.060 nuevos emisores agresivos de facturas falsas y efectividad de sanción penal (80,5%).
* **Capacidades Institucionales:** Distribución de la dotación de 4.913 funcionarios del SII por escalafón y cobertura de los 9.593 cupos del Plan de Formación Institucional (PFI 2026).

---

## Estructura del Repositorio e Instalación Local

| Archivo | Descripción Técnica |
| :--- | :--- |
| `app.py` | Motor principal en Streamlit con los 4 módulos tributarios, simuladores interactivos y gráficos en Plotly. |
| `requirements.txt` | Dependencias de Python necesarias para el despliegue en Streamlit Cloud y ejecución local. |

```bash
git clone https://github.com/mauriciovargas1516-ux/GESTION-TRIBUTARIA-2026.git
cd GESTION-TRIBUTARIA-2026
pip install -r requirements.txt
streamlit run app.py
```
