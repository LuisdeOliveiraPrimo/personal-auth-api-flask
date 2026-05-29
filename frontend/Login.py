import streamlit as st
import requests

URL_API = "http://127.0.0.1:5000"

st.set_page_config(page_title="Login", page_icon="🔒", layout="centered")

# --- MÁGICA DO CSS: Centraliza tudo e esconde a sidebar ---
st.markdown("""
    <style>
    /* Esconde o botão de abrir/fechar sidebar e a própria sidebar */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    /* Centraliza o bloco principal vertical e horizontalmente */
    [data-testid="stAppViewBlockContainer"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    /* Deixa a caixa de conteúdo com um tamanho amigável */
    .stApp > header { display: none; } /* Esconde o cabeçalho superior direito */
    </style>
""", unsafe_allow_html=True)

# Inicia a memória
if 'meu_jwt' not in st.session_state:
    st.session_state['meu_jwt'] = None

# Se já tem token, manda direto para o Dashboard (não deixa ficar na tela de login)
if st.session_state['meu_jwt']:
    st.switch_page("pages/1_🏠_Dashboard.py")

# Layout centralizado da Tela de Login
st.title("🔒 Acesso Restrito")
st.write("Identifique-se para entrar no sistema.")

if st.button("🚀 Entrar (Simular Google)", use_container_width=True):
    dados_simulados = {"email": "luis.oliveiraprimo288@gmail.com", "senha": "sua_senha_secreta"}
    try:
        resposta = requests.post(f"{URL_API}/login", json=dados_simulados)
        if resposta.status_code == 200:
            st.session_state['meu_jwt'] = resposta.json()['token']
            # Joga o usuário direto para a página do Dashboard
            st.switch_page("pages/1_🏠_Dashboard.py")
        else:
            st.error("Acesso negado: Você não tem permissão.")
    except Exception as e:
        st.error("Erro: O servidor Flask não está rodando.")