from flask import render_template, url_for, request, flash, redirect, abort
from googletrans import Translator
from ComunidadeImpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from ComunidadeImpressionadora import app, Database, criptografia
from ComunidadeImpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# Criando a variável de traduzir as mensagens de erro:

traduzir = Translator()

# Route é uma função que está sendo executada, é um decorator, uma função que atribiu a outra função uma nova funcionalidade. Ele vai atribuir uma funcionalidade na função "def homepage":

@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    # O render_template puxa os arquivos que estão dentro da pasta "Template", ou seja, todas as formatações HTML feitas nos arquivos HTMl são exibidas nessa funcionalidade
    return render_template("homepage.html", posts=posts) 

@app.route("/contato suporte")
def contato():
    return render_template("contato.html")

@app.route("/usuario")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", Lista_usuarios=lista_usuarios)

@app.route("/login", methods=["GET", "POST"]) # Permite o usuário a realizar requerimento de informações, com o GET, e postagens de infomrações "POST"
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and "botao_login" in request.form:
        # Verificando se o usuário e senha existem:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and criptografia.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibindo a mensagem de que o login foi efetuado com sucesso:
            flash(f'Login efetuado com sucesso para o usuário: {form_login.email.data}!', 'alert-success') # Exibindo o resultado do que o usuário inseriu no campo de formulário de login
            parametro_next = request.args.get('next') # O request.arg são todos os argumentos que estarão dentro da URL do site "?next=xxxxx", ele pega o parametro que está no argumento em questão, no caso, o next.
            if parametro_next:
                return redirect(parametro_next)
            else:
                    # Redirecionando o usuário para a URL desejada, neste caso sendo a homepage:
                return redirect(url_for('homepage'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos!', 'alert-danger')
        # Fez o login com sucesso:
    if form_criarconta.validate_on_submit() and "botao_criar_conta" in request.form:
        # Senha criptografada:
        senha_cript = criptografia.generate_password_hash(form_criarconta.senha.data)
        # Criar o usuario:
        usuario = Usuario(usuario=form_criarconta.usuario.data, email=form_criarconta.email.data, senha=senha_cript)
        # Adicionar a sessão:
        Database.session.add(usuario)
        # Commit na sessão:
        Database.session.commit()
        flash(f'Conta criada com sucesso para o usuário: {form_criarconta.email.data}!', 'alert-success') # Exibindo o resultado do que o usuário inseriu no campo de formulário de criar conta
        # Redirecionando o usuário para a URL desejada, neste caso sendo a homepage:
        return redirect(url_for('homepage'))
        # Criou a conta com sucesso:
    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta, traduzir=traduzir)

@app.route('/sair')
@login_required
def Sair():
    logout_user()
    flash('Logout realizado com sucesso!', 'alert-success') 
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def Perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) # Criando a variável do local da foto
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET','POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        Database.session.add(post)
        Database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    # Adicionar um código aleatório no nome da imagem:
    codigo = secrets.token_hex(8)
    # Adiciona o código secreto no nome do arquivo
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    # Caminho onde a imagem será salva
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # Reduizr o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduziada = Image.open(imagem)
    imagem_reduziada.thumbnail(tamanho)
    # Salvar a imagem na pasta fotos_perfil
    imagem_reduziada.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if "curso_" in campo.name:
            # Se o campo estiver marcado (for verdadeiro):
            if campo.data:
                # Adicionar o texto do campo.label (Excel Impressionador) na lista de cursos:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/perfil/editar', methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.usuario = form.usuario.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
            # Mudar o campo fotos_perfil do usuario para o novo nome da imagem
        current_user.cursos = atualizar_cursos(form)
        Database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('Perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.usuario.data = current_user.usuario
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) # Criando a variável do local da foto
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form, traduzir=traduzir)

@app.route('/post/<post_id>', methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            Database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('homepage'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        Database.session.delete(post)
        Database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('homepage'))
    else:
        abort(403)