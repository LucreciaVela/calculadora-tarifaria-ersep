
import streamlit as st
import pandas as pd
import io
import xlsxwriter

st.set_page_config(page_title="ERSEP Transporte - Costos Personal", layout="centered")

st.title("ERSEP Transporte - Cálculo Sección A - Costos Asociados al Personal")

st.markdown("### Datos cargados desde Hoja Llave - Columna O")

# Valores extraídos desde la planilla
Pm = 0.4344
Pr = 0.5656
He = 10.0
SHm = 5445.303646
SHr = 5445.303646
IMEm = 1.6
IMEr = 1.6

# Datos ya definidos en cálculo anterior
Mp = 93803.21  # Prima mensual
U = 188544.80  # Indumentaria
Hn = 192
ITDm = 1.1429
Ccm = 2.5
Sbcu = 950000.00
RTM = 6452004.00
Ut = 850
PartM = 0.45

SHm = (Sbcu * 1.1) / 192
km_m = (RTM * Pm) / (Ut * PartM)

Cp1 = (Pm * Hn * SHm * ITDm * Ccm) / km_m
Cp2m = Pm * He * SHm * IMEm
Cp2r = Pr * He * SHr * IMEr
Cp2 = (Cp2m + Cp2r) / km_m
Cp5 = (Pm * Mp) / km_m
Cp6 = 0.18 * (Cp1 + Cp2)
Cp7 = (Pm * U) / km_m

# Construir el resumen
df = pd.DataFrame([
    ["A1", "Horas Hombre del Personal de Conducción", round(Cp1, 2)],
    ["A2", "Incidencia Económica por Horas Extras", round(Cp2, 2)],
    ["A5", "Seguro del Personal", round(Cp5, 2)],
    ["A6", "Viáticos", round(Cp6, 2)],
    ["A7", "Indumentaria", round(Cp7, 2)],
], columns=["Código", "Concepto", "Costo por km"])

st.dataframe(df)

# Exportar a Excel
output = io.BytesIO()
workbook = xlsxwriter.Workbook(output, {'in_memory': True})
worksheet = workbook.add_worksheet("Resumen de Cálculo")

worksheet.write("B1", "CALCULO TARIFARIO A DICIEMBRE 2024")
worksheet.write("B3", "COSTOS ASOCIADOS AL PERSONAL")

for i, row in enumerate(df.itertuples(index=False), start=4):
    worksheet.write(f"B{i}", row.Código)
    worksheet.write(f"C{i}", row.Concepto)
    worksheet.write(f"J{i}", row._2)

workbook.close()
output.seek(0)

st.download_button("📥 Descargar Resumen de Cálculo (.xlsx)",
    data=output,
    file_name="Resumen_Costos_Personal_A.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
