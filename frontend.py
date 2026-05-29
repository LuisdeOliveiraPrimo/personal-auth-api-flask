import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Passo 2: Carregar o arquivo .env (Esta é a linha mágica!)
load_dotenv() 

# Passo 3: Puxar a variável específica usando os.getenv()
ALLOWED_EMAIL = os.getenv('ALLOWED_EMAIL')
minha_senha = os.getenv('ALLOWED_PASSWORD')
chave_jwt = os.getenv('JWT_SECRET_KEY')
URL_API = os.getenv('URL_API')
# Passo 4: Usar a variável no seu código
print(f"O email liberado para acesso é: {ALLOWED_EMAIL}")

# URL do seu servidor Flask
URL_API_1 = URL_API

# 1. Memória do Streamlit
if 'meu_jwt' not in st.session_state:
    st.session_state['meu_jwt'] = None

# 2. Telas
def mostrar_tela_login():
    st.title("🔒 Acesso Restrito")
    st.write("Clique no botão abaixo para autenticar automaticamente.")

    # APENAS UM BOTÃO! Sem campos de texto.
    if st.button("🚀 Entrar (Simular Google)"):
        
        # SIMULAÇÃO: Na vida real, clicar no botão abriria a tela do Google. 
        # Como estamos simulando, mandamos os dados diretamente por baixo dos panos.
        # Altere esta linha dentro do arquivo frontend.py:
        dados_simulados = {{ALLOWED_EMAIL}: "luis.oliveiraprimo288@gmail.com", {minha_senha}: "sua_senha_secreta"}
        
        try:
            resposta = requests.post(f"{URL_API_1}/login", json=dados_simulados)
            
            if resposta.status_code == 200:
                st.session_state['meu_jwt'] = resposta.json()['token']
                st.success("Identidade confirmada! Entrando...")
                st.rerun() 
            else:
                st.error("Acesso negado: Você não tem permissão.")
        except requests.exceptions.ConnectionError:
            st.error("Erro: O servidor Flask (Porteiro) não está rodando.")

def mostrar_tela_home():
    st.title("🏠 Home - Seu Dashboard Privado")
    st.success("Você está logado e o Flask validou seu crachá (JWT)!")
    
    st.write("---")
    st.subheader("Buscando dados secretos...")
    
    # Enviando o JWT para o Flask
    cabecalhos = {'Authorization': f"Bearer {st.session_state['meu_jwt']}"}
    resposta_dados = requests.get(f"{URL_API}/dados-privados", headers=cabecalhos)
    
    if resposta_dados.status_code == 200:
        dados = resposta_dados.json()
        st.write(f"**Mensagem:** {dados['mensagem']}")
        st.json(dados['dados_secretos'])
    else:
        st.error("Sua sessão expirou.")
        
    st.write("---")
    if st.button("Sair (Logout)"):
        st.session_state['meu_jwt'] = None
        st.rerun()

# 3. Roteador
if st.session_state['meu_jwt'] is None:
    mostrar_tela_login()
else:
    mostrar_tela_home()