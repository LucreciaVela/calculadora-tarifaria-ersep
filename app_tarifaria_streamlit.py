
import streamlit as st

st.set_page_config(page_title="Calculadora Tarifaria ERSEP", layout="centered")

st.image("https://www.ersep.cba.gov.ar/wp-content/uploads/2020/09/LogoERSEPColorHorizontal.png", width=300)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Escudo_de_la_Provincia_de_Córdoba.svg/1200px-Escudo_de_la_Provincia_de_Córdoba.svg.png", width=120)

st.title("Calculadora Tarifaria - ERSEP")

st.markdown("### Ingresá los 23 datos desde la Hoja Llave")

datos_entrada = {}
datos_entrada["Dato 1"] = st.number_input("Dato 1", step=0.01)
datos_entrada["Dato 2"] = st.number_input("Dato 2", step=0.01)
datos_entrada["Dato 3"] = st.number_input("Dato 3", step=0.01)
datos_entrada["Dato 4"] = st.number_input("Dato 4", step=0.01)
datos_entrada["Dato 5"] = st.number_input("Dato 5", step=0.01)
datos_entrada["Dato 6"] = st.number_input("Dato 6", step=0.01)
datos_entrada["Dato 7"] = st.number_input("Dato 7", step=0.01)
datos_entrada["Dato 8"] = st.number_input("Dato 8", step=0.01)
datos_entrada["Dato 9"] = st.number_input("Dato 9", step=0.01)
datos_entrada["Dato 10"] = st.number_input("Dato 10", step=0.01)
datos_entrada["Dato 11"] = st.number_input("Dato 11", step=0.01)
datos_entrada["Dato 12"] = st.number_input("Dato 12", step=0.01)
datos_entrada["Dato 13"] = st.number_input("Dato 13", step=0.01)
datos_entrada["Dato 14"] = st.number_input("Dato 14", step=0.01)
datos_entrada["Dato 15"] = st.number_input("Dato 15", step=0.01)
datos_entrada["Dato 16"] = st.number_input("Dato 16", step=0.01)
datos_entrada["Dato 17"] = st.number_input("Dato 17", step=0.01)
datos_entrada["Dato 18"] = st.number_input("Dato 18", step=0.01)
datos_entrada["Dato 19"] = st.number_input("Dato 19", step=0.01)
datos_entrada["Dato 20"] = st.number_input("Dato 20", step=0.01)
datos_entrada["Dato 21"] = st.number_input("Dato 21", step=0.01)
datos_entrada["Dato 22"] = st.number_input("Dato 22", step=0.01)
datos_entrada["Dato 23"] = st.number_input("Dato 23", step=0.01)

if st.button("Calcular Tarifa"):
    total = sum(datos_entrada.values())
    tarifa = total / 23
    st.success(f"Costo Total Estimado: ${round(total, 2)}")
    st.info(f"Tarifa Promedio por Ítem: ${round(tarifa, 2)}")
