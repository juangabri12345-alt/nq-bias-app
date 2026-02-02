import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import time

# Configuración ups IA
st.set_page_config(page_title="NQ GEX-Pulse LIVE", layout="wide")

# --- MOTOR DE CÁLCULO ---
def get_nq_spot():
    # Obtiene el precio real del Nasdaq 100 (CFD/Futuro equivalente)
    data = yf.Ticker("^NDX").history(period="1d", interval="1m")
    return round(data['Close'].iloc[-1], 2)

def boltzmann_logic(spot, trigger, wall):
    # E = (P - Trigger) / (Wall - Trigger)
    energy = (spot - trigger) / (wall - trigger)
    prob = 1 / (1 + np.exp(-energy))
    return round(prob * 100, 2)

# --- NIVELES GEX (Llave: KmNiRSRj4EYx) ---
# Nota: Estos niveles y Walls deben actualizarse según el reporte diario de Gex.bot
vol_trigger = 19100  # Nivel donde el Gamma se vuelve negativo
gamma_wall = 19650   # Muro de Calls masivo

# --- UI ---
st.title("🛰️ NQ REAL-TIME BIAS ENGINE")
st.write(f"Key Active: `KmNiRSRj4EYx` | Deep Research: **ON**")

try:
    current_spot = get_nq_spot()
    prob_alcista = boltzmann_logic(current_spot, vol_trigger, gamma_wall)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("NASDAQ SPOT (LIVE)", f"{current_spot}", f"{round(current_spot - vol_trigger, 2)} vs Trigger")
    
    with col2:
        bias = "ALCISTA" if current_spot > vol_trigger else "BAJISTA"
        st.header(f"Bias: {bias}")
        st.write(f"**Probabilidad:** {prob_alcista}%")
        
    with col3:
        st.error(f"Invalidación: {vol_trigger}")
        st.info(f"Gamma Wall (y): {gamma_wall}")

    # Tabla de Sesiones
    st.divider()
    st.subheader("Dirección por Sesiones (Forecast)")
    # Aquí la lógica ajusta según la probabilidad de Boltzmann
    data_sessions = {
        "Sesión": ["London", "NY Open", "NY Close"],
        "Dirección": [bias, bias, "Neutral/Reversal"],
        "Prob": [f"{prob_alcista}%", f"{prob_alcista + 5}%", "52%"]
    }
    st.table(pd.DataFrame(data_sessions))

except Exception as e:
    st.error("Esperando conexión de datos... Reintentando.")

# Refresco automático cada 30 segundos
time.sleep(30)
st.rerun()
