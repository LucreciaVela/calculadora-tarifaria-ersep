
import streamlit as st

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
datos["Nc"] = st.number_input("Nc - Unidad de valuación (medida 900 r22,5 + recapado)", step=0.01)
datos["Nm"] = st.number_input("Nm - Unidad de valuación (medida 275/80 r22,5 + recapado)", step=0.01)
datos["Ng"] = st.number_input("Ng - Unidad de valuación (medida 295/80 r22,5 + recapado)", step=0.01)
datos["L"] = st.number_input("L - Precio de aceite para motor (tambor de 205 litros)", step=0.01)
datos["Mp"] = st.number_input("Mp - Monto de la prima mensual en pesos", step=0.01)
datos["E"] = st.number_input("E - Costo de lavado y engrase", step=0.01)
datos["Pp"] = st.number_input("Pp - Monto anual de patente ponderado", step=0.01)
datos["RTM"] = st.number_input("RTM - Recorrido Total Mensual", step=0.01)
datos["Sbcu"] = st.number_input("Sbcu - Sueldo básico conducción empresas metropolitanas", step=0.01)
datos["Pm"] = st.number_input("Pm - Porcentaje participación empresas metropolitanas", step=0.01)
datos["Pr"] = st.number_input("Pr - Porcentaje participación empresas rurales", step=0.01)
datos["SBcg"] = st.number_input("SBcg - Sueldo básico conducción empresas rurales", step=0.01)
datos["Gm"] = st.number_input("Gm - Precio Gas Oil empresas metropolitanas", step=0.01)
datos["Gr"] = st.number_input("Gr - Precio Gas Oil empresas rurales", step=0.01)
datos["Vc"] = st.number_input("Vc - Valor unidad nueva chica", step=0.01)
datos["Vm"] = st.number_input("Vm - Valor unidad nueva mediana", step=0.01)
datos["Vg"] = st.number_input("Vg - Valor unidad nueva grande", step=0.01)
datos["RBM"] = st.number_input("RBM - Recaudación Bruta Mensual Promedio", step=0.01)
datos["Ut"] = st.number_input("Ut - Flota total - Unidades (UP-SP-IP)", step=0.01)

if st.button("Ver datos cargados"):
    st.write("Valores ingresados:")
    st.json(datos)
