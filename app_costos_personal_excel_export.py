
import streamlit as st
import pandas as pd
import io
import xlsxwriter

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
datos["Ut"] = st.number_input("Ut - Flota total (todas las unidades)", step=0.01)
datos["PartM"] = st.number_input("PartM - % Participación unidades servicio metropolitano", step=0.01)
datos["Sbcu"] = st.number_input("Sbcu - Sueldo básico conducción", step=0.01)
datos["Pm"] = st.number_input("Pm - % Participación empresas metropolitanas", step=0.01)

if st.button("Calcular Costos Personal (Metropolitanas)"):
    try:
        ITDm = 1.1429
        Ccm = 2.5
        Hn = 192
        Pm = datos["Pm"] / 100
        PartM = datos["PartM"] / 100
        SHm = (datos["Sbcu"] * 1.1) / 192
        km_m = (datos["RTM"] * Pm) / (datos["Ut"] * PartM)

        Cp1 = (Pm * Hn * SHm * ITDm * Ccm) / km_m
        Seguro = (Pm * datos["Mp"]) / km_m
        Indumentaria = (Pm * datos["U"]) / km_m

        df = pd.DataFrame([
            ["Horas Hombre del Personal de Conducción", round(Cp1, 2)],
            ["Seguro del Personal", round(Seguro, 2)],
            ["Indumentaria", round(Indumentaria, 2)]
        ], columns=["Concepto", "Costo por km"])

        st.markdown("### Resumen - Costos Asociados al Personal (Metropolitanas)")
        st.dataframe(df)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Resumen de Cálculo")

        titulo = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'})
        worksheet.merge_range('B1:L1', "CALCULO TARIFARIO A DICIEMBRE 2024", titulo)

        worksheet.write("B3", "COSTOS ASOCIADOS AL PERSONAL", workbook.add_format({'bold': True}))
        worksheet.write("B4", "A1")
        worksheet.write("C4", "Horas Hombre del Personal de Conducción")
        worksheet.write("J4", round(Cp1, 2))

        worksheet.write("B5", "A5")
        worksheet.write("C5", "Seguro del Personal")
        worksheet.write("J5", round(Seguro, 2))

        worksheet.write("B6", "A7")
        worksheet.write("C6", "Indumentaria")
        worksheet.write("J6", round(Indumentaria, 2))

        workbook.close()
        output.seek(0)

        st.download_button("📥 Descargar Resumen de Cálculo (.xlsx)",
            data=output,
            file_name="Resumen_Costos_Metropolitanos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Error en el cálculo: {str(e)}")
