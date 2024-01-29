# Para criar o ambiente virtual com o intuito de utilização e criação do site, você precisar passar os comandos abaixo:

    # CTRL + SHIFT + P --> Cria o ambiente virtual
    # nome-do-ambiente\Scripts\activate --> Altera para o ambiente virtual
    # nome-do-ambiente\Scripts\deactivate --> Desativa o ambiente virtual

# Importando as bibliotecas:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Colocando o site no ar:
    # Método que tem dentro da Classe Flask, cria o site:

app = Flask(__name__)

app.config['SECRET_KEY'] = '8f492823342fedd2f68a1e0e526b5390'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db' # Criando o banco de dados (Será criado no mesmo local do arquivo main)

Database = SQLAlchemy(app)
criptografia = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from ComunidadeImpressionadora import routes