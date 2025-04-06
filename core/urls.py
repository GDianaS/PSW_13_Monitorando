from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')), #incluindo uma lista de urls apos o 'usuarios/'
    path('mentorados/', include('mentorados.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # arquivos de media
