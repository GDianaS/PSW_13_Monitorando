from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User #importar a tabela do banco de dados User

from django.contrib.messages import constants
from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib import auth
# Create your views here.

## VIEW DE CADASTRO
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais.')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deverá ter no mínimo 6 caracteres.')
            return redirect('/usuarios/cadastro')
        
        users = User.objects.filter(username=username) # pega os usernames que já existem na tabela

        if users.exists():#verifica se já existe o dado na tabela
            messages.add_message(request, constants.ERROR, 'Nome de usuário já em uso.')
            return redirect('/usuarios/cadastro')

        User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('/usuarios/login')
    

## VIEW DE LOGIN
def login(request):
    if request.method == 'GET':
        return render (request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user: 
            auth.login(request, user)
            return redirect('/mentorados/')
        
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('login')