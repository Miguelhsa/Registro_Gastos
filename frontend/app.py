import streamlit as st 
import httpx

#st.image("frontend/PHOTO-2026-06-30-09-25-00.jpg")

st.title("AVISADOR DE GASTOS")

st.write("Hola! Introduzca su categoria y su gasto")

password = st.text_input("password de entrada", type="password")

categoria = st.text_input("Categoría del gasto")

importe = st.number_input("Cantidad gastada")

boton = st.button("mandar gasto", type="primary")

if boton:
    
    respuesta = httpx.post("http://127.0.0.1:8000/registrar", json={"categoria": categoria,"importe":importe},headers={"X-API-Key": password})
    if respuesta.status_code == 200:
        st.write("Gasto enviado!")
    else: 
        st.error(respuesta.text)