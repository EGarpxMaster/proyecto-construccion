import streamlit as st
import pandas as pd
import pulp
import altair as alt
import os

st.set_page_config(layout="wide", page_title="Simulación y Optimización de Recursos")

# ===========================
# Título
# ===========================
st.title("📈 Dashboard Interactivo de Simulación y Optimización")

# ===========================
# Carga de Datos
# ===========================
dataset_path = os.path.join("datos", "dataset_construccion.csv")
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
else:
    st.error(f"No se encontró el archivo en: {dataset_path}")
    st.stop()

# ===========================
# Sliders en Sidebar
# ===========================
st.sidebar.header("Ajuste de Factores")
material_factor_sim = st.sidebar.slider("Factor Materiales (%)", 50, 150, 100)
mano_obra_factor_sim = st.sidebar.slider("Factor Mano de Obra (%)", 50, 150, 100)
presupuesto_factor_sim = st.sidebar.slider("Factor Presupuesto (%)", 50, 150, 100)
presupuesto_global = st.sidebar.slider("Presupuesto Global (%)", 100, 300, 300)

# ===========================
# Simulación de Retrasos
# ===========================
df_sim = df.copy()
df_sim["Retraso Simulado"] = df["Retraso (días)"] + \
    (100 - material_factor_sim) * 0.1 + \
    (100 - mano_obra_factor_sim) * 0.1 + \
    (100 - presupuesto_factor_sim) * 0.05

# ===========================
# Optimización de Recursos
# ===========================
prob = pulp.LpProblem("Minimizar_Retrasos", pulp.LpMinimize)
factor_mat = pulp.LpVariable("Factor_Materiales", lowBound=50, upBound=150, cat='Continuous')
factor_mo = pulp.LpVariable("Factor_Mano_Obra", lowBound=50, upBound=150, cat='Continuous')
factor_pres = pulp.LpVariable("Factor_Presupuesto", lowBound=50, upBound=150, cat='Continuous')
prob += 0.1*(100 - factor_mat) + 0.1*(100 - factor_mo) + 0.05*(100 - factor_pres)
prob += factor_mat + factor_mo + factor_pres <= presupuesto_global
prob.solve()

if pulp.LpStatus[prob.status] == "Optimal":
    mat_opt = factor_mat.varValue
    mo_opt = factor_mo.varValue
    pres_opt = factor_pres.varValue
    retraso_simulado_optimo = 10 + 0.1*(100 - mat_opt) + 0.1*(100 - mo_opt) + 0.05*(100 - pres_opt)
    retrasos_optimos = [retraso_simulado_optimo]*len(df_sim)
else:
    st.error("No se encontró una solución óptima para el presupuesto seleccionado.")

# ===========================
# Layout de Gráficas Distribuido
# ===========================
# Columna 1: Métricas + Barras
# Columna 2: Histograma + Línea
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔹 Factores Óptimos y Métricas")
    st.metric("Materiales Óptimo", f"{mat_opt:.1f}%")
    st.metric("Mano de Obra Óptima", f"{mo_opt:.1f}%")
    st.metric("Presupuesto Óptimo", f"{pres_opt:.1f}%")

    df_bar = pd.DataFrame({
        "Factor": ["Materiales", "Mano de Obra", "Presupuesto"],
        "Valor": [mat_opt, mo_opt, pres_opt]
    })
    chart_bar = alt.Chart(df_bar).mark_bar().encode(
        x="Factor:N",
        y=alt.Y("Valor:Q", title="Porcentaje"),
        color=alt.Color("Factor:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c"])),
        tooltip=["Factor","Valor"]
    ).properties(height=350, title="Asignación Óptima de Recursos")
    st.altair_chart(chart_bar, use_container_width=True)
    st.markdown("**Descripción:** Barras que representan la asignación óptima de recursos según la optimización lineal.")

with col2:
    st.subheader("🔹 Distribución y Evolución de Retrasos")
    
    # Histograma
    chart_hist = alt.Chart(df_sim).mark_bar(opacity=0.7, color="#69b3a2").encode(
        x=alt.X("Retraso Simulado:Q", bin=alt.Bin(maxbins=20), title="Retraso Simulado (días)"),
        y=alt.Y('count():Q', title="Frecuencia"),
        tooltip=['count()']
    ).properties(height=200, title="Distribución de Retrasos Simulados")
    st.altair_chart(chart_hist, use_container_width=True)
    st.markdown("**Descripción:** Muestra cómo se distribuyen los retrasos simulados entre los proyectos.")

    # Línea de comparación
    df_line = pd.DataFrame({
        "Proyecto ID": df["Proyecto ID"],
        "Retraso Simulado": df_sim["Retraso Simulado"],
        "Retraso Óptimo": retrasos_optimos
    })
    df_melted = df_line.melt(id_vars=["Proyecto ID"], var_name="Tipo", value_name="Valor")
    chart_line = alt.Chart(df_melted).mark_line(point=True).encode(
        x="Proyecto ID:N",
        y=alt.Y("Valor:Q", title="Retraso (días)"),
        color="Tipo:N",
        tooltip=["Proyecto ID","Tipo","Valor"]
    ).properties(height=300, title="Retrasos Simulados vs Óptimos")
    st.altair_chart(chart_line, use_container_width=True)
    st.markdown("**Descripción:** Compara los retrasos simulados con los retrasos calculados usando los factores óptimos.")

