import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="IndiGo Ops Command Center",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE "BLACK" THEME (Custom CSS) ---
st.markdown("""
    <style>
    /* Main Background to Black */
    .stApp {
        background-color: #0e1117; /* Very dark grey/black */
        color: #ffffff;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        color: #4B9CD3; /* Bright Blue for contrast */
        font-weight: 700;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Metric Cards (Darker containers) */
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        color: white;
        border: 1px solid #374151;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #333;
    }
    
    /* Success/Error Message Text Fix */
    .stAlert {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar: Flight Simulation Controls ---
st.sidebar.markdown("# ✈️ Flight Simulator")
st.sidebar.markdown("---")

# Inputs
origin = st.sidebar.selectbox("Origin Airport", ["DEL", "BOM", "BLR", "CCU"])
dest = st.sidebar.selectbox("Destination Airport", ["BOM", "BLR", "CCU", "DEL"])
aircraft = st.sidebar.selectbox("Aircraft Type", ["A320", "A321", "ATR-72"])

st.sidebar.subheader("👨‍✈️ Crew Status (FDTL)")
pilots_req = st.sidebar.slider("Pilots Required", 2, 4, 2)
pilots_avail = st.sidebar.slider("Pilots Available", 0, 5, 2)
avg_duty = st.sidebar.slider("Avg Crew Duty Hours", 0.0, 14.0, 8.5)

# --- 4. Logic Layer ---
def get_prediction(req, avail, duty):
    # Simulated Logic (Replicating your notebook model)
    pilot_shortage = req - avail
    peak_duty_flag = 1 if duty > 9 else 0
    
    score = 0.1
    if pilot_shortage > 0: score += 0.6
    if peak_duty_flag: score += 0.25
    
    return {
        "status": "CANCELLED" if score > 0.5 else "ON_TIME",
        "risk": min(score * 100, 99),
        "shortage": pilot_shortage
    }

if st.sidebar.button("Analyze Flight Risk"):
    with st.spinner("Accessing Ops Mainframe..."):
        time.sleep(1) 
        data = get_prediction(pilots_req, pilots_avail, avg_duty)
        
        # --- 5. Main Dashboard Layout ---
        st.markdown('<p class="main-header">Operational Risk Dashboard</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("### 🚦 Prediction")
            if data['status'] == "CANCELLED":
                st.error(f"🛑 {data['status']}")
            else:
                st.success(f"✅ {data['status']}")
            
            # Using standard Streamlit metric (styled by CSS above)
            st.metric("Pilot Shortage", f"{max(0, data['shortage'])}")
            
        with col2:
            st.markdown("### 📉 Live Risk Monitor")
            
            # DARK THEME GAUGE CHART
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = data['risk'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                number = {'font': {'color': "white"}}, # White number
                title = {'text': "Cancellation Probability", 'font': {'color': "white", 'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00BFFF"}, # Neon Blue needle
                    'bgcolor': "black",
                    'borderwidth': 2,
                    'bordercolor': "#333",
                    'steps': [
                        {'range': [0, 40], 'color': "#1b4f25"}, # Dark Green
                        {'range': [40, 70], 'color': "#5e4b16"}, # Dark Orange
                        {'range': [70, 100], 'color': "#5c1313"}], # Dark Red
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            
            # Make Plotly Background Transparent to blend with black page
            fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"})
            
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### ⚠️ Key Drivers")
            st.info(f"Duty Hours: {avg_duty}h")
            
            if avg_duty > 9:
                st.warning("Violation: Duty > 9h")
            elif data['shortage'] > 0:
                st.error("Critical: Crew Missing")
            else:
                st.success("Drivers: Normal")

else:
    st.markdown('<p class="main-header">IndiGo Ops Command Center</p>', unsafe_allow_html=True)
    st.markdown("Waiting for input...")
    st.image("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", caption="Live Ops View")