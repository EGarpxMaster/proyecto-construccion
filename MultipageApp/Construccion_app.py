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
""")

# Fórmula principal del modelo
st.markdown("**Fórmula del Modelo:**")
st.latex(r"""
R_{simulado} = R_{original} + \sum_{i=1}^{3} w_i \cdot \max(0, 1 - f_i) \cdot R_{original}
""")

st.markdown("""
Donde:
- $R_{simulado}$ = Retraso simulado (días)
- $R_{original}$ = Retraso original del proyecto (días)
- $w_i$ = Peso del recurso $i$ (Materiales, Mano de Obra, Presupuesto)
- $f_i$ = Factor del recurso $i$ (0.5 a 1.5, donde 1.0 = 100%)
- $\max(0, 1 - f_i)$ = Solo penaliza cuando hay déficit de recursos ($f_i < 1$)
""")

st.markdown("**Pesos de Impacto por Defecto:**")
st.latex(r"""
\begin{align}
w_{materiales} &= 0.4 \\
w_{mano\_obra} &= 0.5 \\
w_{presupuesto} &= 0.3
\end{align}
""")

st.markdown("""
- **Justificación:** Este enfoque de primer orden permite una evaluación rápida y clara de la sensibilidad de los proyectos a cada tipo de recurso.

##### 3) Métricas de Impacto Clave
""")

# Métricas con fórmulas
st.markdown("**Retraso Total Simulado:**")
st.latex(r"""
RT = \sum_{j=1}^{n} R_{simulado,j}
""")
st.markdown("Donde $n$ es el número total de proyectos en el portafolio.")

st.markdown("**Retraso Promedio Simulado:**")
st.latex(r"""
RP = \frac{1}{n} \sum_{j=1}^{n} R_{simulado,j}
""")

st.markdown("**Eficiencia Temporal Simulada:**")
st.latex(r"""
ET = \frac{\text{Número de proyectos con } R_{simulado} \leq 0}{n} \times 100\%
""")

st.markdown("**Índice de Impacto de Recursos:**")
st.latex(r"""
IIR = \frac{RT_{simulado} - RT_{original}}{RT_{original}} \times 100\%
""")
st.markdown("Este índice muestra el cambio porcentual en el retraso total respecto a la línea base.")

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

**Tip estratégico:**
Utiliza el simulador para justificar solicitudes de presupuesto adicional, demostrando cuantitativamente cómo una inversión específica puede reducir los retrasos y mejorar la eficiencia general del portafolio.
""")

###################################
# Función de ejemplo para el cálculo
###################################
st.subheader("Ejemplo de Implementación del Modelo")

# Ejemplo de cálculo
st.markdown("**Ejemplo de Cálculo:**")
st.markdown("Para un proyecto con retraso original de 10 días:")

# Valores de ejemplo
factor_materiales = 0.8  # 80%
factor_mano_obra = 0.7   # 70%
factor_presupuesto = 1.2 # 120%

w_mat, w_mo, w_pres = 0.4, 0.5, 0.3
retraso_original = 10

# Cálculo paso a paso
impacto_mat = w_mat * max(0, 1 - factor_materiales) * retraso_original
impacto_mo = w_mo * max(0, 1 - factor_mano_obra) * retraso_original
impacto_pres = w_pres * max(0, 1 - factor_presupuesto) * retraso_original

retraso_simulado = retraso_original + impacto_mat + impacto_mo + impacto_pres

st.latex(f"""
\\begin{{align}}
\\text{{Impacto Materiales}} &= 0.4 \\times \\max(0, 1 - 0.8) \\times 10 = 0.4 \\times 0.2 \\times 10 = {impacto_mat:.1f} \\text{{ días}} \\\\
\\text{{Impacto Mano de Obra}} &= 0.5 \\times \\max(0, 1 - 0.7) \\times 10 = 0.5 \\times 0.3 \\times 10 = {impacto_mo:.1f} \\text{{ días}} \\\\
\\text{{Impacto Presupuesto}} &= 0.3 \\times \\max(0, 1 - 1.2) \\times 10 = 0.3 \\times 0 \\times 10 = {impacto_pres:.1f} \\text{{ días}} \\\\
R_{{\text{{simulado}}}} &= 10 + {impacto_mat:.1f} + {impacto_mo:.1f} + {impacto_pres:.1f} = {retraso_simulado:.1f} \\text{{ días}}
\\end{{align}}
""")

st.markdown(f"""
**Interpretación:** Con materiales al {factor_materiales*100:.0f}%, mano de obra al {factor_mano_obra*100:.0f}% y presupuesto al {factor_presupuesto*100:.0f}%, 
el retraso aumenta de {retraso_original} días a {retraso_simulado:.1f} días. El exceso de presupuesto (120%) no compensa 
automáticamente los déficits en otros recursos en este modelo.
""")

st.divider()