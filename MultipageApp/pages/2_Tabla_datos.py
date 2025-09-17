import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Tabla de Datos", layout="wide")

ROOT = Path(__file__).resolve().parents[1] 
DATA = ROOT / "datos" / "dataset_construccion.csv"  

if not DATA.exists():
    raise FileNotFoundError(f"No se encontró el archivo de datos en: {DATA}")

st.title("Tabla de datos")
st.divider()
st.write("Los datos que exploraremos están disponibles en la siguiente tabla:")

df = pd.read_csv(DATA)
st.dataframe(df)
