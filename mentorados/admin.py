from django.contrib import admin
from .models import Navigators, Mentorados, DisponibilidadedeHorarios, Reuniao

# Register your models here.

admin.site.register(Navigators)
admin.site.register(Mentorados)
admin.site.register(DisponibilidadedeHorarios)
admin.site.register(Reuniao)

