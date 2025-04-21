
import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
from datetime import datetime
import os

# Encabezado con fecha automática
meses_es = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}
hoy = datetime.now()
encabezado = f"CÁLCULO TARIFARIO A {meses_es[hoy.month]} {hoy.year}"

st.set_page_config(page_title="ERSeP - Final Visual", layout="wide")
st.title("📊 Cálculo Tarifario ERSeP")
st.markdown(f"### {encabezado}")

EXCEL_FILE = "Incremento TBK_ Mesa 13 Octubre 2025.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error("❌ No se encuentra el archivo base.")
    st.stop()

try:
    df_raw = pd.read_excel(EXCEL_FILE, sheet_name="Resumen de Calculo", header=None)
except Exception as e:
    st.error(f"Error al leer hoja 'Resumen de Calculo': {e}")
    st.stop()

# Buscar fila donde empieza la tabla real (donde esté el título "CALCULO TARIFARIO A...")
fila_inicio = df_raw[df_raw.iloc[:, 0].astype(str).str.contains("CALCULO TARIFARIO", na=False)].index.min()

if pd.isna(fila_inicio):
    st.error("❌ No se encontró el encabezado de la tabla principal.")
    st.stop()

# Leer desde 2 filas debajo (encabezado + datos)
df = df_raw.iloc[fila_inicio + 2:, :6]
df.columns = ["Código", "Ítem de costo", "Valor calculado", "% Incidencia", "Valor vigente", "Variación %"]
df = df.dropna(subset=["Código", "Ítem de costo"], how="all")

# Formatear valores
def fmt_decimal(val):
    try:
        return f"{float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return val

def fmt_pct(val):
    try:
        return f"{float(val):.1f}".replace(".", ",") + " %"
    except:
        return val

df["Valor calculado"] = df["Valor calculado"].apply(fmt_decimal)
df["% Incidencia"] = df["% Incidencia"].apply(fmt_pct)
df["Valor vigente"] = df["Valor vigente"].apply(fmt_decimal)
df["Variación %"] = df["Variación %"].apply(fmt_pct)

st.success("✅ Tabla de cálculo cargada correctamente.")
st.dataframe(df, use_container_width=True, hide_index=True)

# Exportar con estilo
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Resumen")
    wb = writer.book
    ws = writer.sheets["Resumen"]
    formato = wb.add_format({"border": 1})
    for col in range(len(df.columns)):
        ws.set_column(col, col, 28, formato)

st.download_button(
    label="📥 Descargar tabla con diseño aprobado",
    data=output.getvalue(),
    file_name="Resumen_Tarifario_ERSEP_Diseño_OK.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
