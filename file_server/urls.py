from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'file_server'

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.sign_in, name='login'),
    path('sign_out', views.sign_out, name='logout'),
    re_path(r'media/*', views.protected_serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)