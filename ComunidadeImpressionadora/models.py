# Criando as tabelas do banco de dados:

from ComunidadeImpressionadora import Database
from datetime import datetime
from ComunidadeImpressionadora import login_manager
from flask_login import UserMixin

# Criando uma função que busca o ID do usuário:

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(Database.Model, UserMixin):
    id = Database.Column(Database.Integer, primary_key=True)
    usuario = Database.Column(Database.String, nullable=False) # O campo de usuario deve sempre estar preenchido
    email = Database.Column(Database.String, nullable=False, unique=True) # Este valor tem de ser único na tabela
    senha = Database.Column(Database.String, nullable=True)
    foto_perfil = Database.Column(Database.String, default="default.jpg")
    posts = Database.relationship('Post', backref='autor', lazy=True)
    cursos = Database.Column(Database.String, nullable=False, default='Não informado')
    
    def contar_posts(self):
        return len(self.posts)

class Post(Database.Model):
    id = Database.Column(Database.Integer, primary_key=True)
    titulo = Database.Column(Database.String, nullable=False)
    corpo = Database.Column(Database.Text, nullable=False)
    data_criacao = Database.Column(Database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = Database.Column(Database.Integer, Database.ForeignKey('usuario.id'), nullable=False)