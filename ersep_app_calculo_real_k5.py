
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Datos de entrada y descripción
descripcion_variables = {
    "MT": "Monto anual de la prima para personal de conducción",
    "U": "Costo de los uniformes según convenio",
    "Nc": "Valuación neumático 900 r22.5",
    "Nm": "Valuación neumático 275/80 r22.5",
    "Ng": "Valuación neumático 295/80 r22.5",
    "L": "Costo de lubricantes anualizado",
    "Mp": "Mantenimiento preventivo anual"
}

# Cálculo real de K5
def calcular_k5(datos):
    try:
        return (datos["MT"] * datos["U"] * datos["Nc"] * datos["Nm"] * datos["Ng"] * datos["L"]) / datos["Mp"]
    except ZeroDivisionError:
        return 0

# App visual
meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
         "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
hoy = datetime.now()
st.set_page_config(page_title="ERSeP Cálculo K5", layout="wide")
st.title("🚌 Cálculo Interno ERSeP – Fórmula K5")
st.markdown(f"### CÁLCULO TARIFARIO A {meses[hoy.month - 1]} {hoy.year}")
st.markdown("#### Ingreso de datos variables")

# Inputs
inputs = {}
cols = st.columns(3)
for i, cod in enumerate(descripcion_variables):
    label = f"{cod} – {descripcion_variables[cod]}"
    with cols[i % 3]:
        inputs[cod] = st.number_input(label, value=1000.00, format="%.2f", step=100.0)

# Cálculo y resultado
if st.button("🔍 Calcular fórmula K5"):
    resultado_k5 = calcular_k5(inputs)
    resultado_fmt = f"{resultado_k5:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.success(f"✅ Resultado fórmula K5: {resultado_fmt}")

    # Tabla resumen
    df = pd.DataFrame([{
        "Código": "K5",
        "Ítem de costo": "Cálculo fórmula real (K5)",
        "Valor calculado": resultado_fmt,
        "% Incidencia": "100 %",
        "Valor vigente": "—",
        "Variación %": "—"
    }])

    st.dataframe(df, use_container_width=True, hide_index=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Resumen")
        wb = writer.book
        ws = writer.sheets["Resumen"]
        fmt = wb.add_format({"border": 1})
        for col in range(len(df.columns)):
            ws.set_column(col, col, 28, fmt)

    st.download_button(
        label="📥 Descargar resumen con diseño",
        data=output.getvalue(),
        file_name="Resumen_Tarifario_K5.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
