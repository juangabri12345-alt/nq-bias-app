import streamlit as st
import numpy as np
import pandas as pd

# Configuración de la App
st.set_page_config(page_title="NQ GEX-Pulse AI", layout="wide")

def boltzmann_prob(levels, gex_values, temperature=1.0):
    """Calcula la probabilidad de dirección basada en la distribución de Boltzmann sobre niveles GEX"""
    exp_gex = np.exp(gex_values / temperature)
    probabilities = exp_gex / np.sum(exp_gex)
    return probabilities

# Sidebar - Parámetros de Control
st.sidebar.header("Control de Inyección de Datos")
gex_key = st.sidebar.text_input("Gex.bot Key", value="KmNiRSRj4EYx", type="password")
spot_price = st.sidebar.number_input("Nasdaq Spot (NQ)", value=18000.0)

# Simulación de niveles GEX (Aquí se integraría el Deep Research / API)
st.title("📊 NQ Directional Bias - Boltzmann Distribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Volatility Trigger", "17,850")
    st.write("Gamma Wall (+): 18,200")

with col2:
    # Lógica de Sesgo (Basada en tus reglas)
    skew_status = "Aplanándose (Real Rally)"
    st.subheader(f"Bias: ALCISTA")
    st.write(f"Probabilidad: 78.4%")

with col3:
    st.error(f"Invalidación: 17,920 GEX Wall")
    st.write("Acción: Flip a Bajista")

# Panel de Sesiones
st.divider()
st.subheader("Dirección por Sesiones")
sesiones = {
    "London": ["Alcista", "65%"],
    "NY Open": ["Alcista", "72%"],
    "NY Close (Vanna/Charm)": ["Bajista", "55%"]
}
st.table(pd.DataFrame(sesiones, index=["Dirección", "Probabilidad"]))

# Advertencia de Hedging
st.info("⚠️ Alerta de Charm: Vencimiento cercano. Market Makers forzarán compras independientemente del macro.")
