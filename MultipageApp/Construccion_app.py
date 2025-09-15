import streamlit as st
import pandas as pd
import numpy as np
import os

st.title("Simulación de Asignación de Recursos en Construcción")

###################################
# Introducción
###################################
st.subheader("Introducción")
st.markdown("""
Este panel de simulación permite **analizar y cuantificar** el impacto de la asignación de recursos en los cronogramas de proyectos de construcción. La gestión eficiente de **materiales, mano de obra y presupuesto** es crítica para minimizar retrasos y asegurar la rentabilidad.

**Propósito:** entregar una herramienta interactiva para que los gestores de proyectos puedan **modelar escenarios hipotéticos**, comprender las sensibilidades del proyecto y tomar decisiones informadas para optimizar la asignación de recursos.
""")

st.divider()

###################################
# ¿Qué es este simulador?
###################################
st.subheader("¿Qué es este simulador?")
st.markdown("""
Es una herramienta que aplica un **modelo matemático determinista** para calcular cómo las variaciones en la disponibilidad de recursos afectan los retrasos de un portafolio de proyectos. Ayuda a responder, entre otras, las siguientes preguntas:

- ¿Cuál es el impacto en el **retraso total** si sufrimos un recorte presupuestario del 15%?
- ¿Podemos compensar una **escasez de mano de obra** aumentando la inversión en materiales?
- ¿Qué **combinación de recursos** minimiza los retrasos promedio en todos los proyectos?
- ¿Cómo cambia la **eficiencia temporal** (proyectos terminados a tiempo) al variar los factores?
""")

st.divider()

###################################
# Modelo y Funcionalidades
###################################
st.subheader("Modelo y Funcionalidades")

st.markdown("""
##### 1) Controles de Simulación
- **Factores de Recursos:** Tres controles deslizantes permiten ajustar la disponibilidad de **Materiales**, **Mano de Obra** y **Presupuesto** en un rango de 50% (escasez severa) a 150% (abundancia). El 100% representa la línea base del proyecto original.

##### 2) Modelo de Cálculo
- **Relación Lineal:** El "Retraso Simulado" se calcula a partir del retraso original, añadiendo un impacto proporcional a la desviación de cada recurso respecto a la línea base. El modelo asume que una reducción de recursos incrementa linealmente el retraso, basado en pesos predefinidos.
- **Justificación:** Este enfoque de primer orden permite una evaluación rápida y clara de la sensibilidad de los proyectos a cada tipo de recurso.

##### 3) Métricas de Impacto Clave
- **Retraso Total Simulado:** La suma de los días de retraso de todos los proyectos en el escenario actual.
- **Retraso Promedio Simulado:** El promedio de retraso por proyecto, para entender el impacto general.
- **Eficiencia Temporal Simulada:** El porcentaje de proyectos que se completarían a tiempo o antes de lo previsto (retraso <= 0).
""")

st.divider()

###################################
# Guía de uso
###################################
st.subheader("Guía de uso")
st.markdown("""
1. **Analiza la Línea Base:** Con todos los factores en 100%, las métricas reflejan el estado original de los datos.
2. **Modela un Escenario:** Desliza los controles para simular cambios. Por ejemplo, reduce el "Factor de Mano de Obra" al 80% para ver el efecto de una escasez.
3. **Observa los Resultados:** Revisa cómo cambian las métricas en tiempo real. Fíjate en el aumento del retraso total y la caída de la eficiencia.
4. **Busca el Equilibrio:** Intenta compensar un déficit (ej. menos materiales) con un superávit en otro (ej. más presupuesto) y encuentra un escenario óptimo que cumpla tus objetivos.

**Tip estratégico**
Utiliza el simulador para justificar solicitudes de presupuesto adicional, demostrando cuantitativamente cómo una inversión específica puede reducir los retrasos y mejorar la eficiencia general del portafolio.
""")

st.divider()

# --- A PARTIR DE AQUÍ VA EL CÓDIGO DE LA SIMULACIÓN ---

# Cargar datos
# (Este código es un placeholder, asegúrate de que la ruta sea correcta para tu entorno)
try:
    # Intenta una ruta relativa común para Streamlit
    base_path = os.path.dirname(__file__)
    dataset_path = os.path.join(base_path, "datos", "dataset_construccion.csv")
    df = pd.read_csv(dataset_path)
except (NameError, FileNotFoundError):
    # Fallback para cuando no se puede encontrar el archivo (ej. en un entorno de prueba)
    st.warning("No se pudo cargar el archivo `dataset_construccion.csv`. Se usarán datos de ejemplo.")
    data = {'Proyecto ID': ['PROY-001', 'PROY-002', 'PROY-003'],
            'Tipo de Obra': ['Puente', 'Edificio', 'Carretera'],
            'Retraso (días)': [10, -5, 22],
            'Materiales Usados (ton)': [500, 2000, 1500],
            'Mano de Obra (horas)': [8000, 25000, 18000],
            'Presupuesto ($)': [1000000, 5000000, 3000000]}
    df = pd.DataFrame(data)