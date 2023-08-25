from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'file_server'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-file', views.upload_file, name='upload_file'),
    path('delete/files/<int:file_id>', views.delete_file, name='delete_file'),
    path('sign-in', views.sign_in, name='login'),
    path('sign-out', views.sign_out, name='logout'),
    path('sign-up', views.sign_up, name='signup'),
    re_path(r'media/*', views.protected_serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)