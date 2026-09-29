import streamlit as st

# Configuración visual de la aplicación
st.set_page_config(
    page_title="Critical Care Infusion Manager",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado básico
st.markdown("""
    <style>
    .main-header { font-size:2rem; font-weight:700; color:#1E3A8A; }
    .sub-header { font-size:1.1rem; color:#4B5563; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🩺 Critical Care Infusion Manager</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculadora clínica de precisión para infusión continua e inótropos</p>',
            unsafe_allow_html=True)
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
# TAB 1: VASOPRESORES E INÓTROPICOS
# ==========================================
with tab_vaso:
    fármaco = st.selectbox(
        "Seleccione el vasoactivo:",
        ["Norepinefrina", "Adrenalina (Epinefrina)", "Vasopresina", "Dobutamina"]
    )

    st.divider()

    if fármaco == "Norepinefrina":
        st.subheader("🔴 Norepinefrina")
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown("##### Configuración de la Mezcla")
            ampollas = st.number_input("Ampollas (4 mg / 4 ml):", value=2, min_value=1)
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5%):", value=250)

            total_mg = ampollas * 4
            conc_mcg_ml = (total_mg * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({total_mg} mg en {volumen_ml} ml)")

        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=0.01, max_value=2.00, value=0.10, step=0.01)
                flujo = (dosis * peso * 60) / conc_mcg_ml

                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis > 0.5:
                    st.warning("⚠️ Dosis alta de Norepinefrina. Evalúe inicio de segundo vasopresor (ej. Vasopresina).")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=10.0, step=0.5)
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} mcg/kg/min")

    elif fármaco == "Adrenalina (Epinefrina)":
        st.subheader("⚡ Adrenalina (Epinefrina)")
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown("##### Configuración de la Mezcla")
            ampollas = st.number_input("Ampollas (1 mg / 1 ml):", value=4, min_value=1)
            volumen_ml = st.number_input("Volumen dilución (ml DAD 5% / SSN):", value=250)

            total_mg = ampollas * 1
            conc_mcg_ml = (total_mg * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({total_mg} mg en {volumen_ml} ml)")

        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=0.01, max_value=1.00, value=0.05, step=0.01)
                flujo = (dosis * peso * 60) / conc_mcg_ml

                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
                if dosis <= 0.05:
                    st.caption("🔵 Predominio β1/β2 (Efecto inótropo/cronótropo).")
                else:
                    st.caption("🔴 Predominio α1 (Efecto vasopresor predominante).")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=5.0, step=0.5)
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} mcg/kg/min")

    elif fármaco == "Vasopresina":
        st.subheader("💧 Vasopresina")
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown("##### Configuración de la Mezcla")
            unidades = st.number_input("Unidades totales (UI):", value=20, step=10)
            volumen_ml = st.number_input("Volumen dilución (ml SSN 0.9%):", value=100)

            conc_ui_ml = unidades / volumen_ml
            st.info(f"**Concentración final:** `{conc_ui_ml:.3f} UI/ml` ({unidades} UI en {volumen_ml} ml)")

        with c2:
            st.markdown("##### Parámetros de Infusión (Dosis Fija)")
            st.caption("Nota: La Vasopresina habitualmente se dosifica de forma fija (no ajustada por peso).")

            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis_ui_min = st.select_slider(
                    "Dosis objetivo (UI/min):",
                    options=[0.01, 0.02, 0.03, 0.04, 0.06],
                    value=0.03
                )
                flujo = (dosis_ui_min * 60) / conc_ui_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=9.0, step=0.5)
                dosis_calc = (flujo_input * conc_ui_ml) / 60
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.3f} UI/min")

    elif fármaco == "Dobutamina":
        st.subheader("🫀 Dobutamina")
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown("##### Configuración de la Mezcla")
            mg_totales = st.number_input("Dobutamina total (mg):", value=250)
            volumen_ml = st.number_input("Volumen total (ml):", value=250)

            conc_mcg_ml = (mg_totales * 1000) / volumen_ml
            st.info(f"**Concentración final:** `{conc_mcg_ml:.2f} mcg/ml` ({mg_totales} mg en {volumen_ml} ml)")

        with c2:
            st.markdown("##### Parámetros de Infusión")
            if modo_calculo == "Dosis ➔ Velocidad (ml/h)":
                dosis = st.slider("Dosis objetivo (mcg/kg/min):", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
                flujo = (dosis * peso * 60) / conc_mcg_ml
                st.metric(label="⚙️ Velocidad de Bomba", value=f"{flujo:.1f} ml/h")
            else:
                flujo_input = st.number_input("Velocidad en bomba (ml/h):", min_value=0.1, value=15.0, step=0.5)
                dosis_calc = (flujo_input * conc_mcg_ml) / (peso * 60)
                st.metric(label="📊 Dosis Administrada", value=f"{dosis_calc:.2f} mcg/kg/min")

# ==========================================
# TAB 2: SEDACIÓN Y ANALGESIA
# ==========================================
with tab_sed:
    st.subheader("🧠 Propofol / Sedación")
    st.info("Próximamente: Propofol 1%, Dexmedetomidina, Fentanilo y Midazolam.")

# ==========================================
# TAB 3: VASODILATADORES
# ==========================================
with tab_vasodil:
    st.subheader("🫀 Vasodilatadores")
    st.info("Próximamente: Nitroglicerina y Nitroprusiato de Sodio.")