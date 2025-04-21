
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Valores fijos desde Excel
Pm = 0.4344
Hn = 192
SHm = 5445.3036
IL = 1.2308
ITDm = 1.0667
Cem = 2.5

def calcular_cp1_m(km_m):
    try:
        numerador = Pm * Hn * SHm * IL * ITDm * Cem
        return numerador / km_m
    except ZeroDivisionError:
        return 0

# Interfaz
st.set_page_config(page_title="Cálculo Cp1 (m)", layout="wide")
st.title("🚌 Cálculo Cp1 (m) – Componente parcial A1 (modo metro)")
st.markdown("#### Ingresá el valor de km(m) – Kilometraje mensual medio recorrido por empresas metropolitanas")

km_m = st.number_input("km (m) – Kilometraje medio mensual metropolitano", value=7266.02, format="%.2f", min_value=1.0)

if st.button("🔍 Calcular Cp1 (m)"):
    resultado = calcular_cp1_m(km_m)
    resultado_fmt = f"{resultado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.success(f"✅ Resultado Cp1 (m): {resultado_fmt}")

    df = pd.DataFrame([{
        "Código": "Cp1(m)",
        "Ítem de costo": "Cp1 (m) – Cálculo parcial HH personal conducción (modo metro)",
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
            ws.set_column(col, col, 30, fmt)

    st.download_button(
        label="📥 Descargar resultado en Excel",
        data=output.getvalue(),
        file_name="Cp1_m_Calculado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
