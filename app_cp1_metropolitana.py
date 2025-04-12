
import streamlit as st

st.set_page_config(page_title="Calculadora Tarifaria ERSEP", layout="centered")

st.title("Calculadora Tarifaria - ERSEP")
st.markdown("### Cálculo del Cp1 (m) - Empresas Metropolitanas")

datos = {}

datos["Pm"] = st.number_input("Pm - Porcentaje de participación de empresas metropolitanas", step=0.01)
datos["Hn"] = st.number_input("Hn - Cantidad de horas netas abonadas por mes", step=0.01)
datos["SHm"] = st.number_input("SHm - Sueldo básico de convenio conductor guarda único", step=0.01)
datos["IL"] = st.number_input("IL - Coeficiente de horas pagas y no trabajadas", step=0.01)
datos["ITDm"] = st.number_input("ITDm - Coeficiente de tome y deje de servicio", step=0.01)
datos["Ccm"] = st.number_input("Ccm - Cantidad de conductores por unidad (metropolitanas)", step=0.01)
datos["km (m)"] = st.number_input("km (m) - Kilometraje mensual medio recorrido por coche metropolitano", step=0.01)

if st.button("Calcular Cp1 (m)"):
    try:
        Pm = datos["Pm"]
        Hn = datos["Hn"]
        SHm = datos["SHm"]
        IL = datos["IL"]
        ITDm = datos["ITDm"]
        Ccm = datos["Ccm"]
        km_m = datos["km (m)"]

        resultado = (Pm * Hn * SHm * IL * ITDm * Ccm) / km_m
        st.success(f"Cp1 (m) = {round(resultado, 2)}")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
