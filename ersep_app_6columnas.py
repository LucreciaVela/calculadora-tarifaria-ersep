
# ERSEP TRANSPORTE APP - Cálculo Tarifario
# Versión estructural base con 6 columnas y subtotales por CP

import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
from datetime import datetime

# Fecha actual
meses_es = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}
hoy = datetime.now()
encabezado = f"CÁLCULO TARIFARIO A {meses_es[hoy.month]} {hoy.year}"

st.set_page_config(page_title="Calculadora ERSeP Transporte", layout="wide")
st.title("🚌 Calculadora Tarifaria ERSeP Transporte")
st.markdown(f"### {encabezado}")
st.markdown("**(Diseño visual de tabla con 6 columnas)**")

# Ejemplo visual de la tabla que se verá en la app
data = {
    "Código": ["A1", "A2", "A3", "Subtotal A", "B1", "B2", "Subtotal B"],
    "Nombre del costo": [
        "Sueldo conductor", "Cargas sociales", "Indemnización",
        "Subtotal personal",
        "Neumáticos", "Combustible",
        "Subtotal vehículo"
    ],
    "Valor calculado": [1500000, 700000, 300000, 2500000, 800000, 1500000, 2300000],
    "% Incidencia": [30.0, 14.0, 6.0, 50.0, 16.0, 34.0, 50.0],
    "Valor vigente": [1200000, 680000, 250000, 2130000, 760000, 1400000, 2160000],
    "Variación %": [25.0, 2.9, 20.0, 17.4, 5.3, 7.1, 6.5]
}
df = pd.DataFrame(data)

st.dataframe(df.style.format({
    "Valor calculado": "{:,.0f}",
    "% Incidencia": "{:.1f} %",
    "Valor vigente": "{:,.0f}",
    "Variación %": "{:.1f} %"
}), use_container_width=True)

# Botón de descarga simulado
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Resumen')
st.download_button(
    label="📥 Descargar ejemplo de tabla",
    data=output.getvalue(),
    file_name="Resumen_Tarifario_Ejemplo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
