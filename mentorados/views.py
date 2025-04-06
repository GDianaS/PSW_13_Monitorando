from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .auth import valida_token
from .models import Mentorados, Navigators, DisponibilidadedeHorarios, Reuniao, Tarefa, Upload  # permite usar as variaveis das classes em models

from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime, timedelta

from .auth import valida_token
# Create your views here.
def mentorados(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'GET':
        navigators = Navigators.objects.filter (user=request.user) # navigators do usuário que está logado
        mentorados = Mentorados.objects.filter(user=request.user)

        estagios_flat = [i[1] for i in Mentorados.estagio_choices] # valores
        qtd_estagios = [] # quantidade de pessoas por estágio

        for i, j in Mentorados.estagio_choices:
            qtd_estagios.append(Mentorados.objects.filter(estagio=i).count())

        return render(request, 'mentorados.html', {'estagios':Mentorados.estagio_choices, 'navigators': navigators, 'mentorados': mentorados, 'estagios_flat': estagios_flat, 'qtd_estagios':qtd_estagios})
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        estagio = request.POST.get("estagio")
        navigator = request.POST.get('navigator')

        mentorado = Mentorados(
            nome=nome,
            foto=foto,
            estagio=estagio,
            navigator_id=navigator,
            user=request.user
        )

        mentorado.save()

        messages.add_message(request, constants.SUCCESS, 'Mentorado cadastrado com sucesso.')
        return redirect('mentorados')

def reunioes(request):
    if request.method == 'GET':
        reunioes = Reuniao.objects.filter(data__mentor=request.user)
        return render (request, 'reunioes.html', {'reunioes': reunioes})
    elif request.method == 'POST':
        data = request.POST.get('data')
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        #__gte : maior ou igual
        #__lte : menor ou igual
        disponibilidade = DisponibilidadedeHorarios.objects.filter(
            data_inicial__gte=(data - timedelta(minutes=50)),
            data_inicial__lte=(data + timedelta(minutes=50))
        )

        if disponibilidade.exists():
            messages.add_message(request, constants.ERROR, 'Você já possui uma reunião em aberto.')
            return redirect('reunioes')

        # Salvar no banco de dados
        disponibilidade = DisponibilidadedeHorarios(
            data_inicial=data,
            mentor=request.user
        )

        disponibilidade.save()

        messages.add_message(request, constants.SUCCESS, 'Horário disponibilizado com sucesso.')
        return redirect('reunioes')


def auth(request):
    if request.method == 'GET':
        return render(request, 'auth_mentorado.html')
    elif request.method == 'POST':
        token = request.POST.get('token')

        if not Mentorados.objects.filter(token=token).exists():
            messages.add_message(request, constants.ERROR, 'Token inválido')
            return redirect('auth_mentorado')

        response = redirect('escolher_dia')
        # cookies: usados para guardar informações
        response.set_cookie('auth_token', token, max_age=3600)
        return response

def escolher_dia(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')

    if request.method == 'GET':
        mentorado = valida_token(request.COOKIES.get('auth_token')) # mentorado que digitou o cookie

        disponibilidades = DisponibilidadedeHorarios.objects.filter(
            data_inicial__gte = datetime.now(),
            agendado = False,
            mentor = mentorado.user
        ).values_list('data_inicial', flat=True)

        datas = []
        for i in disponibilidades:
            datas.append(i.date().strftime('%d-%m-%Y'))

        #TODO: Mês e dia da semana dinâmicos no html

        return render(request, 'escolher_dia.html', {'horarios': list(set(datas))})

def agendar_reuniao(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')

    mentorado = valida_token(request.COOKIES.get('auth_token'))

    #TODO: Validar se o horário agendado é realmente de um mentor do mentorado

    if request.method == 'GET':
        data = request.GET.get('data') # parametro vem da url
        data = datetime.strptime(data, '%d-%m-%Y')

        # horarios disponiveis para o dia
        horarios = DisponibilidadedeHorarios.objects.filter(
            data_inicial__gte = data,
            data_inicial__lt = data + timedelta(days=1),
            agendado=False,
            mentor = mentorado.user
        )
        return render(request, 'agendar_reuniao.html', {'horarios': horarios, 'tags': Reuniao.tag_choices})

    else:
        horario_id = request.POST.get('horario')
        tag = request.POST.get('tag')
        descricao = request.POST.get('descricao')

        reuniao = Reuniao(
            data_id = horario_id,
            mentorado=mentorado,
            tag = tag,
            descricao = descricao,
        )

        reuniao.save()

        #TODO: Atomicidade

        #Marca a disponibilidade de horário como False:
        horario = DisponibilidadedeHorarios.objects.get(id=horario_id)
        horario.agendado = True
        horario.save()

        messages.add_message(request, constants.SUCCESS, 'Reunião agendada com sucesso.')
        return redirect('escolher_dia')

def tarefa(request, id):
    mentorado = Mentorados.objects.get(id = id)

    if mentorado.user != request.user:
        raise Http404()

    if request.method == 'GET':
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
        videos = Upload.objects.filter(mentorado=mentorado)

        return render(request, 'tarefa.html', {'mentorado': mentorado, 'tarefas': tarefas, 'videos': videos})

    else:
        tarefa = request.POST.get('tarefa')

        #TODO: Validação se não é um texto vazio ou se tem um máximo de caracteres

        t = Tarefa(
            mentorado=mentorado,
            tarefa = tarefa
        )

        t.save()

        return redirect(f'/mentorados/tarefa/{id}')


def upload(request, id):
    mentorado = Mentorados.objects.get(id=id)
    if mentorado.user != request.user:
        raise Http404()

    video = request.FILES.get('video')
    upload = Upload(
        mentorado=mentorado,
        video=video
    )
    upload.save()
    return redirect(f'/mentorados/tarefa/{mentorado.id}')