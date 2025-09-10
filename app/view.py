from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import UserForm, LoginForm, EmprestimoForm, LivroForm
from app.models import User, Emprestimo, Livro
from app import bcrypt
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import String
from flask import flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('livro_lista'))
        else:
            return render_template('index.html', form=form, erro="Usuário ou senha incorretos.")
    return render_template('index.html', form=form)

@app.route('/')
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('livro_lista'))
    else:
        return render_template('home.html')


@app.route('/registeruser/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('livro_lista'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/livros/')
@login_required
def livro_lista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Livro.query.order_by('genero')
    
    if pesquisa != '':
        dados = dados.filter(Livro.titulo.ilike(f'%{pesquisa}%'))
    
    livros = {'dados' : dados.all()}
    return render_template('livro_lista.html', livros=livros)

@app.route('/cadastrolivro/', methods=['GET', 'POST'])
@login_required
def livro_novo():
    form = LivroForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('livro_lista'))
    return render_template('livro_novo.html', context=context, form=form) 

@app.route('/emprestimo/')
@login_required
def emprestimo_lista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Emprestimo.query.order_by('user_id')
    
    if pesquisa != '':
        dados = dados.filter(cast(Emprestimo.user_id, String).ilike(f'%{pesquisa}%'))
    
    hoje = datetime.now() 
    
    emprestimos = {'dados' : dados.all(), 'hoje': hoje}
    return render_template('emprestimo_lista.html', emprestimos=emprestimos)


@app.route('/cadastroemprestimo/', methods=['GET', 'POST'])
@login_required
def emprestimo_novo():
    form = EmprestimoForm()
    context = {}
    if form.validate_on_submit():
        emprestimo = form.save()
        if emprestimo is None:
            flash('Não há exemplares disponíveis para empréstimo deste livro.', 'danger')
            return render_template('emprestimo_novo.html', context=context, form=form)
        else:
            flash('Empréstimo realizado com sucesso!', 'success')
            return redirect(url_for('emprestimo_lista'))
    return render_template('emprestimo_novo.html', context=context, form=form)