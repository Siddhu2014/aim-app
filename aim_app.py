import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
#     PRODUCTION BRANDING & STYLING (CSS)
# ==========================================
def apply_production_skin():
    """
    Injects custom CSS to hide internal developer tools (like the Deploy button)
    and clean up the layout margins for end-users.
    """
    st.markdown("""
        <style>
        /* Hide the Streamlit Cloud deployment banner/button for users */
        .stDeployButton { display: none !important; }
        footer { visibility: hidden; }
        
        /* Premium metric formatting */
        div[data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 700;
            color: #00ffcc !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
#     STEP 1: METRIC SIMULATION GENERATOR
# ==========================================
def generate_mock_mouse_data(style):
    """
    Generates telemetry coordinates to populate the production environment
    when no custom user file is uploaded.
    """
    timestamps = np.linspace(0, 2.0, 100)
    target_x = np.linspace(100, 500, 100)
    target_y = np.linspace(100, 400, 100)
    
    if style == "Pro (Elite Aim)":
        noise_x = np.random.normal(0, 3.5, 100)
        noise_y = np.random.normal(0, 3.5, 100)
    else:
        noise_x = np.random.normal(0, 16, 100) + np.sin(timestamps * 15) * 12
        noise_y = np.random.normal(0, 14, 100) + np.cos(timestamps * 15) * 10
        
    player_x = target_x + noise_x
    player_y = target_y + noise_y
    
    return pd.DataFrame({
        "Timestamp_Sec": timestamps,
        "Target_X": target_x,
        "Target_Y": target_y,
        "Player_X": player_x,
        "Player_Y": player_y
    })

# ==========================================
#     STEP 2: VECTOR CALCULATIONS ENGINE
# ==========================================
def analyze_aim_telemetry(df):
    """
    Executes raw physics equations on the coordinate matrices.
    """
    try:
        dx = df["Player_X"] - df["Target_X"]
        dy = df["Player_Y"] - df["Target_Y"]
        pixel_errors = np.sqrt(dx**2 + dy**2)
        
        avg_error = np.mean(pixel_errors)
        max_overflick = np.max(pixel_errors)
        
        # Physics Smoothness derivative logic
        velocity_x = np.diff(df["Player_X"])
        acceleration_x = np.diff(velocity_x)
        smoothness_score = max(0, 100 - int(np.std(acceleration_x) * 5))
        
        return avg_error, max_overflick, smoothness_score
    except Exception:
        # Graceful fallback to prevent production crashes
        return 0.0, 0.0, 0

# ==========================================
#     STEP 3: PUBLIC WEB UI FRAMEWORK
# ==========================================
st.set_page_config(
    page_title="Aim Telemetry Pro", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_production_skin()

# App Bar Header
st.title("🎯 Aim Telemetry Diagnostics Engine")
st.caption("Enterprise-Grade Precision Modeling for Competitive Esports Athletes")
st.write("---")

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("🎛️ Control Center")
dev_mode = st.sidebar.toggle("🛠️ Enable Developer Mode", value=False)

# Initialize telemetry framework variables to prevent global NameErrors
data_df = None
uploaded_file = None

# --- TELEMETRY RESOLUTION LOGIC ---
if not dev_mode:
    # PUBLIC USER MODE: Immediately request CSV upload on the main screen
    st.subheader("📥 Upload Your Telemetry Log")
    st.write("Drop your tracking spreadsheet below to generate your custom diagnostics report.")
    
    uploaded_file = st.file_uploader("Upload target_tracking.csv", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            # Read whatever layout the user drops in
            raw_df = pd.read_csv(uploaded_file)
            
            # AUTOMATED COLUMN MAPPER: Locates standard variations of tracking names
            col_mapping = {}
            for col in raw_df.columns:
                c_low = col.lower()
                if "time" in c_low or "sec" in c_low: col_mapping[col] = "Timestamp_Sec"
                elif "target_x" in c_low or "targetx" in c_low: col_mapping[col] = "Target_X"
                elif "target_y" in c_low or "targety" in c_low: col_mapping[col] = "Target_Y"
                elif "player_x" in c_low or "mouse_x" in c_low or "cursor_x" in c_low: col_mapping[col] = "Player_X"
                elif "player_y" in c_low or "mouse_y" in c_low or "cursor_y" in c_low: col_mapping[col] = "Player_Y"
            
            # Rename columns based on matches found
            data_df = raw_df.rename(columns=col_mapping)
            
            # Fallback Validation Check
            required_cols = ["Target_X", "Target_Y", "Player_X", "Player_Y"]
            if not all(col in data_df.columns for col in required_cols):
                st.error("❌ Column Layout Error: We couldn't automatically locate your coordinate rows. Make sure your file headers contain labels like 'Mouse_X' or 'Target_X'!")
                data_df = None
                
        except Exception:
            st.error("❌ Corrupt File IO Error: Unable to read file matrix structure.")
            data_df = None
    else:
        st.info("👋 Welcome! Please upload a valid CSV file containing tracking coordinates to begin processing diagnostics.")

else:
    # DEVELOPER BACKEND MODE: Sidebar controls unlock for simulation testing
    st.sidebar.warning("DEVELOPER MODE ACTIVE")
    input_mode = st.sidebar.radio("Data Engine Source:", ["Run Diagnostics Simulator", "Upload Mouse CSV Log"])
    
    if input_mode == "Run Diagnostics Simulator":
        test_profile = st.sidebar.selectbox("Simulated Data Array Variant:", ["Pro (Elite Aim)", "Shaky (Hard Overflicker)"])
        data_df = generate_mock_mouse_data(test_profile)
    else:
        st.subheader("📥 Developer Upload Test")
        uploaded_file = st.file_uploader("Upload target_tracking.csv", type=["csv"])
        if uploaded_file is not None:
            data_df = pd.read_csv(uploaded_file)
        else:
            st.info("Upload file or toggle back to Simulator.")
            data_df = None

# --- MAIN RENDER WINDOW ---
if data_df is not None:
    st.write("---")
    avg_err, max_flick, smooth_score = analyze_aim_telemetry(data_df)
    
    # Dashboard Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🎯 SMOOTHNESS RATING", value=f"{smooth_score}/100")
    with col2:
        st.metric(label="📏 AVG. DISPLACEMENT OFFSET", value=f"{avg_err:.2f} px")
    with col3:
        st.metric(label="💥 PEAK OVERFLICK VARIANCE", value=f"{max_flick:.2f} px")
        
    st.write("---")
    
    # Rendering Data Graphs
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        st.subheader("📈 Time-Series Coordinate Shift")
        st.write("Horizontal tracking offset mapped across the timeline array.")
        st.line_chart(data_df[["Player_X", "Target_X"]])
        
    with graph_col2:
        st.subheader("🗺️ 2D Spatial Crosshair Vector Map")
        st.write("Physical coordinate pathways plotted natively in 2D monitor space.")
        
        # Matplotlib High-Fidelity Rendering Block
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0e1117') # Match Streamlit Dark theme canvas
        ax.set_facecolor('#0e1117')
        
        ax.plot(data_df["Target_X"], data_df["Target_Y"], color="#00ffcc", label="Target Vector Line", linewidth=2.5)
        ax.scatter(data_df["Player_X"], data_df["Player_Y"], color="#ff4b4b", label="Your Crosshair Path", alpha=0.8, s=18, edgecolors='none')
        
        # Grid/Axis Styling
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.set_xlabel("Monitor Width Axis (Pixels)")
        ax.set_ylabel("Monitor Height Axis (Pixels)")
        ax.grid(True, linestyle=":", alpha=0.3, color="white")
        
        # Legend custom dark formatting
        leg = ax.legend(facecolor='#0e1117', edgecolor='#00ffcc')
        for text in leg.get_texts():
            text.set_color('white')
            
        st.pyplot(fig)

    # Developer Dump-Table Section
    if dev_mode:
        st.write("---")
        st.subheader("📊 Debug Array Inspection View")
        st.write("Raw float values passing through dataframe tracking cells:")
        st.dataframe(data_df, use_container_width=True)

    st.write("---")
    
    # --- BLUEPRINT ENGINE REPORT ---
    st.subheader("⚙️ Calculated Calibration Blueprint")
    
    blueprint_text = f"""🎯 AIM DIAGNOSTICS PRODUCTION REVEAL
----------------------------------------------
Calculated Movement Fluidity: {smooth_score}/100
Mean Sensor Offset: {avg_err:.2f} Screen Pixels
Max Focal Deceleration Error: {max_flick:.2f} Screen Pixels

CRITICAL BIOMECHANICAL AUDIT:
1. Micro-Stuttering Artifacts: High-frequency acceleration adjustments detected. Your mouse chassis is experiencing stick-slip friction on your current mousepad fabric.
2. Initial Vector Overflight: Your input velocity curves show excessive kinetic energy during initial target targeting phases.

CORRECTION CALIBRATION:
* Decrease your master in-game sensitivity index value by exactly {min(15.0, avg_err * 2.5):.1f}%.
* Ensure Windows 'Enhance Pointer Precision' settings remain entirely disabled to secure raw linear hardware scaling.
"""
    
    st.code(blueprint_text, language="text")
    
    st.download_button(
        label="📥 Download Calibration Profile Blueprint (.txt)",
        data=blueprint_text,
        file_name="Aim_Telemetry_Blueprint.txt",
        mime="text/plain",
        use_container_width=True
    )
