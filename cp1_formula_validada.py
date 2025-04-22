
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Cp1 (m)", layout="centered")

st.title("🧮 Calculadora Cp1 (m) – Subcomponente de A1")

st.markdown("### Ingresá los valores requeridos:")

# Datos de entrada
Pm = st.number_input("Pm – Participación metropolitana", value=0.4344, format="%.4f")
RTM = st.number_input("RTM – Recorrido total mensual", value=6452004.00, format="%.2f")

# Constantes de la fórmula (valores fijos)
Hn = 192
SHm = 5445.3036
IL = 1.2308
ITDm = 1.0667
Ccm = 2.5

# Cálculo de km(m)
km_m = RTM * Pm

# Cálculo Cp1(m)
try:
    Cp1_m = (Pm * Hn * SHm * IL * ITDm * Ccm) / km_m
    Cp1_m = round(Cp1_m, 5)
    resultado_df = pd.DataFrame([{
        "Código": "Cp1(m)",
        "Ítem de costo": "Cp1 (m) – Subcomponente de A1 fórmula validada",
        "Valor calculado": Cp1_m,
        "% Incidencia": "—",
        "Valor vigente": "—",
        "Variación %": "—"
    }])
    st.success(f"✅ Resultado Cp1 (m): {Cp1_m}")
    st.dataframe(resultado_df, hide_index=True)

    # Descargar resultado
    def convertir_excel(df):
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Resultado")
        return buffer.getvalue()

    excel_data = convertir_excel(resultado_df)
    st.download_button("📥 Descargar resultado en Excel", data=excel_data,
                       file_name="resultado_cp1_m.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

except ZeroDivisionError:
    st.error("Error: km(m) no puede ser cero. Verificá los valores ingresados.")
