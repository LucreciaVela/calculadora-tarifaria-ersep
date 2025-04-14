
import streamlit as st
import pandas as pd

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

# Ingreso de datos variables
datos["MT"] = st.number_input("MT - Monto anual de la prima para personal de conducción", step=0.01)
datos["U"] = st.number_input("U - Costo de los uniformes según convenio", step=0.01)
datos["Mp"] = st.number_input("Mp - Monto de la prima mensual en pesos", step=0.01)
datos["E"] = st.number_input("E - Costo de lavado y engrase", step=0.01)
datos["RTM"] = st.number_input("RTM - Recorrido Total Mensual", step=0.01)
datos["Sbcu"] = st.number_input("Sbcu - Sueldo básico del convenio - Metros", step=0.01)
datos["Pm"] = st.number_input("Pm - Porcentaje participación empresas metropolitanas", step=0.0001)
datos["SHm_base"] = st.number_input("O32 - Valor base para SHm", step=0.01)
datos["Hn"] = st.number_input("Hn - Horas netas abonadas por mes", step=1.0)
datos["ITDm"] = st.number_input("ITDm - Coeficiente de tome y deje de servicio", step=0.0001)
datos["Ccm"] = st.number_input("Ccm - Cantidad de conductores por unidad", step=0.01)
datos["km_m"] = st.number_input("km (m) - Kilometraje mensual medio recorrido", step=0.01)

# Cálculo si todos los datos están cargados
if st.button("Calcular Costos Personal (Metropolitanas)"):
    try:
        SHm = (datos["SHm_base"] * 1.1) / 192
        Cp1 = (datos["Pm"] * datos["Hn"] * SHm * datos["ITDm"] * datos["Ccm"]) / datos["km_m"]
        Seguro = (datos["Pm"] * datos["Mp"]) / datos["km_m"]
        Indumentaria = (datos["Pm"] * datos["U"]) / datos["km_m"]

        df = pd.DataFrame({
            "Concepto": [
                "Horas Hombre del Personal de Conducción",
                "Seguro del Personal",
                "Indumentaria"
            ],
            "Costo por km": [round(Cp1, 2), round(Seguro, 2), round(Indumentaria, 2)]
        })

        st.markdown("### Resumen - Costos Asociados al Personal (Metropolitanas)")
        st.dataframe(df)

        # Botón de descarga Excel
        excel = df.to_excel(index=False, engine="xlsxwriter")
        st.download_button("📥 Descargar resumen en Excel", data=excel, file_name="costos_personal_metropolitanas.xlsx")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
