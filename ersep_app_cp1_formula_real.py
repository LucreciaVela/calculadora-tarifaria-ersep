
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Datos fijos según modelo Excel
Hn = 192
SHm = 5445.3036
IL = 1.2308
ITDm = 1.0667
Cem = 2.5

def calcular_cp1_m(Pm, RTM):
    try:
        km_m = RTM * Pm
        numerador = Pm * Hn * SHm * IL * ITDm * Cem
        return numerador / km_m
    except ZeroDivisionError:
        return 0

# Interfaz visual
st.set_page_config(page_title="ERSeP Cp1(m)", layout="wide")
st.title("🚌 Cálculo de Cp1 (m) – Horas Hombre Personal de Conducción")
st.markdown("#### Ingresá los valores de participación metropolitana (Pm) y recorrido total mensual (RTM)")

cols = st.columns(2)
with cols[0]:
    Pm = st.number_input("Pm – Participación de empresas metropolitanas", min_value=0.0001, max_value=1.0, value=0.4344, format="%.4f")
with cols[1]:
    RTM = st.number_input("RTM – Recorrido total mensual", min_value=1.0, value=7266.02, format="%.2f")

if st.button("🔍 Calcular Cp1 (m)"):
    resultado = calcular_cp1_m(Pm, RTM)
    resultado_fmt = f"{resultado:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.success(f"✅ Resultado Cp1 (m): {resultado_fmt}")

    df = pd.DataFrame([{
        "Código": "A1",
        "Ítem de costo": "Horas Hombre del Personal de Conducción",
        "Valor calculado": resultado_fmt,
        "% Incidencia": "—",
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
        label="📥 Descargar resultado en Excel",
        data=output.getvalue(),
        file_name="Cp1_m_Calculado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
