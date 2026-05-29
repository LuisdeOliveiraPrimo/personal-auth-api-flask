import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv() 

ALLOWED_EMAIL = os.getenv('ALLOWED_EMAIL')
minha_senha = os.getenv('ALLOWED_PASSWORD')
chave_jwt = os.getenv('JWT_SECRET_KEY')
URL_API = os.getenv('URL_API')
URL_API = os.getenv('URL_API')

st.set_page_config(page_title="Login", page_icon="🔒")

# Inicia a memória do JWT
if 'meu_jwt' not in st.session_state:
    st.session_state['meu_jwt'] = None

if st.session_state['meu_jwt'] is None:
    st.title("🔒 Acesso Restrito")
    st.write("Bem-vindo ao sistema. Autentique-se para continuar.")
    
    if st.button("🚀 Entrar (Simular Google)"):
        dados_simulados = {"email": ALLOWED_PASSWORD, "senha": ALLOWED_PASSWORD}
        try:
            resposta = requests.post(f"{URL_API}/login", json=dados_simulados)
            if resposta.status_code == 200:
                st.session_state['meu_jwt'] = resposta.json()['token']
                st.success("Identidade confirmada! Acesse o Dashboard no menu lateral 👈")
            else:
                st.error("Acesso negado: Você não tem permissão.")
        except Exception as e:
            st.error("Erro: O servidor Flask não está rodando.")
else:
    st.title("Olá, Luis! 👋")
    st.success("Seu crachá (JWT) está ativo.")
    st.write("Navegue pelas páginas protegidas usando o menu na barra lateral esquerda.")
    
    if st.button("Sair (Logout)"):
        st.session_state['meu_jwt'] = None
        st.rerun()