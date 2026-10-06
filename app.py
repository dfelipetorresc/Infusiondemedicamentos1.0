import streamlit as st

# Configuración visual de la aplicación
st.set_page_config(
    page_title="Critical Care Infusion Manager",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-header { font-size:2rem; font-weight:700; color:#1E3A8A; }
    .sub-header { font-size:1.1rem; color:#4B5563; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🩺 Critical Care Infusion Manager</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculadora clínica de precisión para infusión continua e inótropos</p>', unsafe_allow_html=True)
st.divider()

# Sidebar: Paciente y Modo
st.sidebar.header("📋 Datos del Paciente")
peso = st.sidebar.number_input("Peso corporal (kg):", min_value=1.0, max_value=250.0, value=70.0, step=0.5)

modo_calculo = st.sidebar.radio(
    "Modo de cálculo:",
    ["Dosis ➔ Velocidad (ml/h)", "Velocidad (ml/h) ➔ Dosis"]
)

st.sidebar.divider()
st.sidebar.caption("⚠️ Herramienta de soporte médico. Verifique siempre los cálculos antes de administrar.")

# Pestañas principales
tab_vaso, tab_sed, tab_vasodil = st.tabs([
    "💉 Vasopresores e Inótropos", 
    "🧠 Sedación y Analgesia", 
    "🫀 Vasodilatadores"
])

# ==========================================
# TAB 1: VASOPRESORES E INÓTROPOS
# ==========================================
with tab_vaso:
    fármaco_v = st.selectbox(
        "Seleccione el vasoactivo:",
        ["Norepinefrina", "Adrenalina (Epinefrina)", "Vasopresina", "Dobutamina"]
    )
    
    st.divider()
    
    if fármaco_v == "Norepinefrina":
        st.subheader("🔴 Norepinefrina")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            ampollas = st.number_input("Ampollas (4 mg / 4 ml):", value=2, min_value=1, key="nor_amp")
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5%):", value=250, key="nor_vol")
            total_mg = ampollas * 4
            conc_mcg_ml = (total_mg * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({total_mg} mg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=0.01, max_value=2.00, value=0.10, step=0.01, key="nor_dos")
                flujo = (dosis * peso * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis > 0.5:
                    st.warning("⚠️ Dosis alta de Norepinefrina. Evalúe inicio de segundo vasopresor (ej. Vasopresina).")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=10.0, step=0.5, key="nor_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} mcg/kg/min")

    elif fármaco_v == "Adrenalina (Epinefrina)":
        st.subheader("⚡ Adrenalina (Epinefrina)")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            ampollas = st.number_input("Ampollas (1 mg / 1 ml):", value=4, min_value=1, key="adr_amp")
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5% / SSN):", value=250, key="adr_vol")
            total_mg = ampollas * 1
            conc_mcg_ml = (total_mg * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({total_mg} mg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=0.01, max_value=1.00, value=0.05, step=0.01, key="adr_dos")
                flujo = (dosis * peso * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis <= 0.05:
                    st.caption("🔵 Predominio β1/β2 (Efecto inótropo/cronótropo).")
                else:
                    st.caption("🔴 Predominio α1 (Efecto vasopresor predominante).")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=5.0, step=0.5, key="adr_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} mcg/kg/min")

    elif fármaco_v == "Vasopresina":
        st.subheader("💧 Vasopresina")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            unidades = st.number_input("Unidades totales (UI):", value=20, step=10, key="vas_ui")
            volumen_ml = st.number_input("Volumen dilución (ml SSN 0.9%):", value=100, key="vas_vol")
            conc_ui_ml = unidades / volumen_ml
            st.info(f"**Concentración final:** `{conc_ui_ml:.3f} UI/ml` ({unidades} UI en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión (Dosis Fija)")
            st.caption("Nota: La Vasopresina habitualmente se dosifica de forma fija (no ajustada por peso).")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_ui_min = st.select_slider(
                    "Dosis objetivo (UI/min):",
                    options=[0.01, 0.02, 0.03, 0.04, 0.06],
                    value=0.03,
                    key="vas_dos"
                )
                flujo = (dosis_ui_min * 60) / conc_ui_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=9.0, step=0.5, key="vas_flj")
                dosis_calc = (flujo_input * conc_ui_ml) / 60
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} UI/min")

    elif fármaco_v == "Dobutamina":
        st.subheader("🫀 Dobutamina")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mg_totales = st.number_input("Dobutamina total (mg):", value=250, key="dob_mg")
            volumen_ml = st.number_input("Volumen total (ml):", value=250, key="dob_vol")
            conc_mcg_ml = (mg_totales * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mg_totales} mg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=1.0, max_value=20.0, value=5.0, step=0.5, key="dob_dos")
                flujo = (dosis * peso * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=15.0, step=0.5, key="dob_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mcg/kg/min")

# ==========================================
# TAB 2: SEDACIÓN Y ANALGESIA
# ==========================================
with tab_sed:
    fármaco_s = st.selectbox(
        "Seleccione el sedante/analgésico:",
        ["Propofol 1%", "Dexmedetomidina", "Fentanilo", "Midazolam"]
    )
    
    st.divider()
    
    if fármaco_s == "Propofol 1%":
        st.subheader("🧠 Propofol 1% (10 mg/ml)")
        st.caption("Administración directa sin dilución previa.")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.info("**Concentración estándar:** `10 mg/ml` (10000 mcg/ml)")
        with c2:
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mg_kg_h = st.slider("Dosis objetivo (mg/kg/h):", min_value=0.3, max_value=5.0, value=2.0, step=0.1, key="prp_dos")
                # Fórmula: (mg/kg/h * peso) / 10 mg/ml
                flujo = (dosis_mg_kg_h * peso) / 10.0
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis_mg_kg_h > 4.0:
                    st.warning("⚠️ Precaución con síndrome de infusión de propofol (PRIS) en dosis prolongadas altas.")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=14.0, step=0.5, key="prp_flj")
                dosis_calc = (flujo_input * 10.0) / peso
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mg/kg/h")

    elif fármaco_s == "Dexmedetomidina":
        st.subheader("💤 Dexmedetomidina")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mcg_totales = st.number_input("Dexmedetomidina total (mcg):", value=200, step=100, key="dex_mcg")
            volumen_ml = st.number_input("Volumen dilución (ml SSN 0.9%):", value=50, key="dex_vol")
            conc_mcg_ml = mcg_totales / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mcg_totales} mcg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mcg_kg_h = st.slider("Dosis objetivo (mcg/kg/h):", min_value=0.2, max_value=1.5, value=0.7, step=0.1, key="dex_dos")
                # Dosis en mcg/kg/h: (dosis * peso) / conc_mcg_ml
                flujo = (dosis_mcg_kg_h * peso) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=8.0, step=0.5, key="dex_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / peso
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mcg/kg/h")

    elif fármaco_s == "Fentanilo":
        st.subheader("💉 Fentanilo")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mcg_totales = st.number_input("Fentanilo total (mcg):", value=1000, step=250, key="fen_mcg")
            volumen_ml = st.number_input("Volumen total (ml):", value=100, key="fen_vol")
            conc_mcg_ml = mcg_totales / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mcg_totales} mcg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mcg_kg_h = st.slider("Dosis objetivo (mcg/kg/h):", min_value=0.5, max_value=10.0, value=1.5, step=0.5, key="fen_dos")
                flujo = (dosis_mcg_kg_h * peso) / conc_mcg_ml
                st.metric(label="⚙️️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=10.0, step=0.5, key="fen_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / peso
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mcg/kg/h")

    elif fármaco_s == "Midazolam":
        st.subheader("😴 Midazolam")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mg_totales = st.number_input("Midazolam total (mg):", value=50, step=10, key="mid_mg")
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5% / SSN):", value=100, key="mid_vol")
            conc_mg_ml = mg_totales / volumen_ml
            st.info(f"**Concentración final:** `{conc_mg_ml:.2f} mg/ml` ({mg_totales} mg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mg_kg_h = st.slider("Dosis objetivo (mg/kg/h):", min_value=0.02, max_value=0.20, value=0.05, step=0.01, key="mid_dos")
                flujo = (dosis_mg_kg_h * peso) / conc_mg_ml
                st.metric(label="⚙️️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=7.0, step=0.5, key="mid_flj")
                dosis_calc = (flujo_input * conc_mg_ml) / peso
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} mg/kg/h")

# ==========================================
# TAB 3: VASODILATADORES
# ==========================================
with tab_vasodil:
    fármaco_vd = st.selectbox(
        "Seleccione el vasodilatador:",
        ["Nitroglicerina (NTG)", "Nitroprusiato de Sodio"]
    )
    
    st.divider()
    
    if fármaco_vd == "Nitroglicerina (NTG)":
        st.subheader("🫀 Nitroglicerina (NTG)")
        st.caption("Nota: La dosificación habitual de NTG es en mcg/min (no ajustada por peso).")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mg_totales = st.number_input("Nitroglicerina total (mg):", value=50, step=10, key="ntg_mg")
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5% / SSN):", value=250, key="ntg_vol")
            conc_mcg_ml = (mg_totales * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mg_totales} mg en {volumen_ml} ml)")
        with c2:
            st.markdown("##### Parámetros de Infusión (Dosis Fija)")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mcg_min = st.slider("Dosis objetivo (mcg/min):", min_value=5, max_value=200, value=20, step=5, key="ntg_dos")
                # Fórmula sin peso: (mcg/min * 60) / conc_mcg_ml
                flujo = (dosis_mcg_min * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=6.0, step=0.5, key="ntg_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / 60
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.1f} mcg/min")

    elif fármaco_vd == "Nitroprusiato de Sodio":
        st.subheader("🔴 Nitroprusiato de Sodio")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mg_totales = st.number_input("Nitroprusiato total (mg):", value=50, step=10, key="nip_mg")
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5%):", value=250, key="nip_vol")
            conc_mcg_ml = (mg_totales * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mg_totales} mg en {volumen_ml} ml)")
            st.caption("🔒 Proteger de la luz (sistema fotoprotegido).")
        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_mcg_kg_min = st.slider("Dosis objetivo (mcg/kg/min):", min_value=0.2, max_value=10.0, value=0.5, step=0.1, key="nip_dos")
                flujo = (dosis_mcg_kg_min * peso * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis_mcg_kg_min > 5.0:
                    st.warning("⚠️ Precaución con toxicidad por tiocianato/cianuro en infusiones prolongadas o a dosis altas.")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=5.0, step=0.5, key="nip_flj")
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mcg/kg/min")
