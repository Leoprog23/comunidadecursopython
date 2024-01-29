# Para criar o ambiente virtual com o intuito de utilização e criação do site, você precisar passar os comandos abaixo:

    # CTRL + SHIFT + P --> Cria o ambiente virtual
    # nome-do-ambiente\Scripts\activate --> Altera para o ambiente virtual
    # nome-do-ambiente\Scripts\deactivate --> Desativa o ambiente virtual

# Importando as bibliotecas:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

# Colocando o site no ar:
    # Método que tem dentro da Classe Flask, cria o site:

app = Flask(__name__)

app.config['SECRET_KEY'] = '8f492823342fedd2f68a1e0e526b5390'
# Criando um banco de dados no servidor online (Railway):
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    # Criando um banco de dados local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db' # Criando o banco de dados (Será criado no mesmo local do arquivo main)

Database = SQLAlchemy(app)
criptografia = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from ComunidadeImpressionadora import models

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table('usuario'):
    with app.app_context():
        Database.drop_all()
        Database.create_all()
        print('Base de dados criada')
else:
    print('Base de dados já existente')

from ComunidadeImpressionadora import routes
