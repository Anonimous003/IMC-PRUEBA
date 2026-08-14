import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# CSS para mostrar el nombre en mayúsculas
if "registros" not in st.session_state:
    st.session_state.registros = []

st.markdown("""
<style>
input {
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# Si todavía no se han enviado los datos
if "enviado" not in st.session_state:
    st.session_state.enviado = False

if not st.session_state.enviado:

    st.title("PRUEBA DE FORMULARIO")

    with st.form("Mi formulario"):
        nombre = st.text_input("Nombre")
        peso = st.number_input("Peso (KG)", min_value=0.0, step=10.0)
        altura = st.number_input("Altura (M)", min_value=0.0, step=0.1)

        genero = st.radio(
            "Género",
            ["Masculino", "Femenino", "Elle pendeje"]
        )

        enviado = st.form_submit_button("Enviar")

    if enviado:

        # Calcular IMC
        imc = peso / (altura ** 2)

        # Conectar con Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credenciales = Credentials.from_service_account_info(
            st.secrets["google"],
            scopes=scopes
        )

        cliente = gspread.authorize(credenciales)

        # Abrir tu Google Sheet
        hoja = cliente.open_by_key(
            "1rZV4xmHaXI-DzQEiTU-6F8iPNg1Xk-JOL-_rj1qqZTE"
        ).sheet1

        # Guardar los datos
        hoja.append_row([
            nombre.upper(),
            genero,
            peso,
            altura,
            round(imc, 2)
        ])

        # Mantener tus datos actuales
        st.session_state.nombre = nombre
        st.session_state.peso = peso
        st.session_state.altura = altura
        st.session_state.genero = genero
        st.session_state.enviado = True
        st.rerun()

# Después de enviar, solamente aparecen los datos
else:
    if st.session_state.altura > 0:
        imc = st.session_state.peso / (st.session_state.altura ** 2)

        # IMC grande y centrado
        st.markdown(
            f"""
            <h1 style="text-align: center; font-size: 100px;">
                IMC: {imc:.2f}
            </h1>
            """,
            unsafe_allow_html=True
        )

        # Imagen dependiendo del IMC
        if imc < 18.5:

            st.subheader("FLACOW")
            st.image("images/bajo_peso.jpeg")
            st.audio("audios/bajo_peso.mp3", autoplay=True)

        elif imc < 25:

            st.subheader("Peso normal")
            st.image("images/normal.jpeg")
            ##st.audio("audios/normal.mp3", autoplay=True)

        elif imc < 30:

            st.subheader("Sobrepeso")
            st.image("images/sobrepeso.jpeg")
            st.audio("audios/sobrepeso.mp3", autoplay=True)

        else:

            st.subheader("Obesidad")
            st.image("images/obesidad.png")
            st.audio("audios/obesidad.mp3", autoplay=True)

##st.subheader("Registros")
##st.dataframe(st.session_state.registros)
