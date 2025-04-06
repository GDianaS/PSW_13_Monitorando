from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import secrets

# Create your models here.
# Criar tabelas

class Navigators(models.Model):
    #Funcionário que acompanha mentorado
    nome = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # mentor

    def __str__(self):
        return self.nome

class Mentorados(models.Model):
    estagio_choices= (
        ('E1', '10-100k'),
        ('E2', '100-500K'),
        ('E3', '500-1000K'),
        ('E4', '1000-2000K')
    )
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='fotos', null = True, blank=True) # salvando na pasta fotos dentro da pasta media, definida em settings.py
    estagio = models.CharField(max_length=2, choices = estagio_choices)
    navigator = models.ForeignKey(Navigators, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=16, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.gerar_token_unico()
        super().save(*args, **kwargs)

    def gerar_token_unico(self):
        while True:
            token = secrets.token_urlsafe(8) # 8 * 1.6
            if not Mentorados.objects.filter(token=token).exists():
                return token

    def __str__(self):
        return self.nome

class DisponibilidadedeHorarios(models.Model):
    data_inicial = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=False)

    def data_final (self):
        # cada horario tem 50 minutos
        return self.data_inicial + timedelta(minutes=50)

class Reuniao(models.Model):
    tag_choices = (
        ('G', 'Gestão'),
        ('M', 'Marketing'),
        ('RH', 'Gestão de pessoas'),
        ('I', 'Impostos')
    )

    data = models.ForeignKey(DisponibilidadedeHorarios, on_delete=models.CASCADE)
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=tag_choices)
    descricao = models.TextField()

# python manage.py makemigrations
# python manage.py migrate


