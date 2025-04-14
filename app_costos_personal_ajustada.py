
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Calculadora Tarifaria ERSEP", layout="centered")

# Logos
col1, col2 = st.columns([3, 1])
with col1:
    st.image("https://www.ersep.cba.gov.ar/wp-content/uploads/2020/09/logo-ersep.png", width=280)
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Escudo_de_la_Provincia_de_Córdoba.svg/800px-Escudo_de_la_Provincia_de_Córdoba.svg.png", width=100)

st.title("Calculadora Tarifaria - ERSEP")
st.markdown("### Ingreso de datos variables (Hoja Llave)")

datos = {}
datos["MT"] = st.number_input("MT - Monto anual de la prima para personal de conducción", step=0.01)
datos["U"] = st.number_input("U - Costo de los uniformes según convenio", step=0.01)
datos["Mp"] = st.number_input("Mp - Monto de la prima mensual en pesos", step=0.01)
datos["RTM"] = st.number_input("RTM - Recorrido Total Mensual", step=0.01)
datos["KmsM"] = st.number_input("KmsM - Recorrido mensual empresas metropolitanas", step=0.01)
datos["Um"] = st.number_input("Um - Flota de empresas metropolitanas", step=0.01)
datos["Sbcu"] = st.number_input("Sbcu - Sueldo básico del convenio del personal de conducción (usado para calcular SHm)", step=0.01)
datos["Pm"] = st.number_input("Pm - Porcentaje de participación de empresas metropolitanas", step=0.01)
datos["Hn"] = st.number_input("Hn - Cantidad de horas netas abonadas por mes", step=0.01)

if st.button("Calcular Costos Personal (Metropolitanas)"):
    try:
        ITDm = 1.1429
        Ccm = 2.5
        SHm = (datos["Sbcu"] * 1.1) / 192
        km_m = datos["KmsM"] / datos["Um"]

        Cp1 = (datos["Pm"] * datos["Hn"] * SHm * ITDm * Ccm) / km_m
        Seguro = (datos["Pm"] * datos["Mp"]) / km_m
        Indumentaria = (datos["Pm"] * datos["U"]) / km_m

        df = pd.DataFrame({{
            "Concepto": [
                "Horas Hombre del Personal de Conducción",
                "Seguro del Personal",
                "Indumentaria"
            ],
            "Costo por km": [round(Cp1, 2), round(Seguro, 2), round(Indumentaria, 2)]
        }})

        st.markdown("### Resumen - Costos Asociados al Personal (Metropolitanas)")
        st.dataframe(df)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Resumen")
        st.download_button("📥 Descargar resumen en Excel", data=buffer.getvalue(), file_name="costos_personal_metropolitanas.xlsx")

    except Exception as e:
        st.error(f"Error en el cálculo: {str(e)}")
