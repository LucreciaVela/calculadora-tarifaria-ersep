
import streamlit as st
import pandas as pd
from io import BytesIO

# Constantes desde la hoja ERSEP
Hn = 192
SHm = 5445.3036
IL = 1.2308
ITDm = 1.0667
Cem = 2.5

def calcular_cp1_m(Pm, RTM):
    try:
        km_m = RTM * Pm
        numerador = Hn * SHm * IL * ITDm * Cem
        return numerador / km_m
    except ZeroDivisionError:
        return 0

# Interfaz Streamlit
st.set_page_config(page_title="Cp1 (m) – ERSeP", layout="wide")
st.title("🚌 Cp1 (m) – Subcomponente del ítem A1 (modo metro)")
st.markdown("### Ingresá los datos variables:")

col1, col2 = st.columns(2)
with col1:
    Pm = st.number_input("Pm – Participación metropolitana", min_value=0.0001, max_value=1.0, value=0.4344, format="%.4f")
with col2:
    RTM = st.number_input("RTM – Recorrido Total Mensual", min_value=1.0, value=6452004.00, format="%.2f")

if st.button("🔍 Calcular Cp1 (m)"):
    resultado = calcular_cp1_m(Pm, RTM)
    resultado_fmt = f"{resultado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.success(f"✅ Resultado Cp1 (m): {resultado_fmt}")

    df = pd.DataFrame([{
        "Código": "Cp1(m)",
        "Ítem de costo": "Cp1 (m) – Subcomponente de A1 validado FINAL",
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
        file_name="Cp1_m_Validado_Final.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
