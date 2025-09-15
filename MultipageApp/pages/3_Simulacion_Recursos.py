import streamlit as st
import pandas as pd
import numpy as np
import os

st.title("🔄 Simulación de Asignación de Recursos")

# Cargar datos
base_path = os.path.dirname(os.path.dirname(__file__))
dataset_path = os.path.join(base_path, "datos", "dataset_construccion.csv")
df = pd.read_csv(dataset_path)

st.markdown("""
Ajusta los parámetros para simular distintos escenarios y observa el impacto en los retrasos y la eficiencia.
""")

# Controles para simular recursos
material_factor = st.slider("Factor de Materiales (%)", 50, 150, 100)
mano_obra_factor = st.slider("Factor de Mano de Obra (%)", 50, 150, 100)
presupuesto_factor = st.slider("Factor de Presupuesto (%)", 50, 150, 100)

# Simulación: modificar recursos y calcular nuevos retrasos
sim_df = df.copy()
sim_df["Materiales Usados (ton)"] = sim_df["Materiales Usados (ton)"] * (material_factor / 100)
sim_df["Mano de Obra (horas)"] = sim_df["Mano de Obra (horas)"] * (mano_obra_factor / 100)
sim_df["Presupuesto ($)"] = sim_df["Presupuesto ($)"] * (presupuesto_factor / 100)

# Simple model: menos recursos = más retraso
sim_df["Retraso Simulado (días)"] = sim_df["Retraso (días)"] + (100 - material_factor) * 0.1 + (100 - mano_obra_factor) * 0.1 + (100 - presupuesto_factor) * 0.05

# Métricas
total_retraso = sim_df["Retraso Simulado (días)"].sum()
promedio_retraso = sim_df["Retraso Simulado (días)"].mean()
ef_tiempo = len(sim_df[sim_df["Retraso Simulado (días)"] <= 0]) / len(sim_df) * 100

st.metric("Retraso Total Simulado", f"{total_retraso:.0f} días")
st.metric("Retraso Promedio Simulado", f"{promedio_retraso:.1f} días")
st.metric("Eficiencia Temporal Simulada", f"{ef_tiempo:.1f}%")

st.dataframe(sim_df[["Proyecto ID", "Tipo de Obra", "Retraso Simulado (días)"]])

st.info("Puedes ajustar los factores para encontrar el escenario óptimo que minimice los retrasos.")
