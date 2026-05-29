import streamlit as st
import requests

URL_API = "http://127.0.0.1:5000"

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# --- MÁGICA DO CSS: Esconde a aba de "Login" do menu lateral ---
st.markdown("""
    <style>
    /* Oculta o primeiro item da lista de páginas da sidebar (que é o Login.py) */
    [data-testid="stSidebarNavItems"] li:nth-child(1) {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Trava de Segurança
if st.session_state.get('meu_jwt') is None:
    st.switch_page("Login.py") # Se não tem token, chuta de volta pro Login

# Conteúdo do Dashboard
st.title("📊 Dashboard de Dados")
st.write("Você está conectado de forma segura!")

cabecalhos = {'Authorization': f"Bearer {st.session_state['meu_jwt']}"}
resposta_dados = requests.get(f"{URL_API}/dados-privados", headers=cabecalhos)

if resposta_dados.status_code == 200:
    dados = resposta_dados.json()
    st.success(f"**Mensagem do Flask:** {dados['mensagem']}")
    st.json(dados['dados_secretos'])
else:
    st.error("Sua sessão expirou ou o token é inválido.")
    
st.write("---")
if st.button("Sair (Logout)", type="primary"):
    st.session_state['meu_jwt'] = None
    st.switch_page("Login.py")