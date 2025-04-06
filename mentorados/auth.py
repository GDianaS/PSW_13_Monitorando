from .models import Mentorados

def valida_token(token):
    # filtrar pelo token de Mentorados, pegar o primeiro item da lista
    return Mentorados.objects.filter(token=token).first()