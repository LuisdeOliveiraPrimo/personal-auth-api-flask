import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Função nativa para ler o arquivo .env sem precisar instalar pacotes extras
def carregar_env():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    chave, valor = linha.split('=', 1)
                    os.environ[chave.strip()] = valor.strip()

# Carrega as variáveis de ambiente antes de iniciar o app
carregar_env()

app = Flask(__name__)

# Puxa as configurações diretamente do arquivo .env de forma segura
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') 
app.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', 'HS256')

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    # Busca o e-mail e a senha permitidos dentro do .env
    email_permitido = os.environ.get('ALLOWED_EMAIL')
    senha_permitida = os.environ.get('ALLOWED_PASSWORD')

    if email == email_permitido and senha == senha_permitida:
        token_de_acesso = create_access_token(identity=email)
        return jsonify(token=token_de_acesso), 200
    
    return jsonify({"erro": "Acesso negado"}), 401

@app.route('/dados-privados', methods=['GET'])
@jwt_required()
def acessar_dados():
    usuario_atual = get_jwt_identity()
    return jsonify({
        "mensagem": f"Bem-vindo, {usuario_atual}!",
        "dados_secretos": ["Relatório de Vendas", "Faturamento Anual", "Métricas de Acesso"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)