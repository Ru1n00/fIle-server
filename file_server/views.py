from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.static import serve
from django.contrib import messages

from .models import File

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user)
        return render(request, 'file_server/index.html', {'files': files})
    
    message = 'You are not logged in'
    messages.info(request, message)
    return render(request, 'file_server/index.html')


@login_required(login_url='file_server:login')
def protected_serve(request, document_root=None):
    if request.user.is_authenticated:
        path_arr = request.path.split('/')
        print(path_arr)
        if len(path_arr) >= 2:
            try:
                file_index = path_arr.index('files')
                user_id = path_arr[file_index + 1]
                if user_id != str(request.user.id):
                    message = 'You are not authorized to view this file'
                    messages.info(request, message)
                    return redirect('file_server:index')
            except:
                message = 'Something went wrong'
                messages.info(request, message)
                return redirect('file_server:index')

        request.path = request.path.replace('/media', '')

        return serve(request, request.path, document_root)
    else:
        message = 'You are not logged in'
        messages.info(request, message)
        return redirect('file_server:login')


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login user
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('file_server:index')
        else:
            message = 'Invalid username or password'
            messages.info(request, message)
            return render(request, 'file_server/sign_in.html', {'form': form})
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('file_server:index')
        return render(request, 'file_server/sign_in.html', {'form': form})
    # return render(request, 'file_server/sign_in.html')


def sign_out(request):
    logout(request)
    return redirect('file_server:index')
    # return render(request, 'file_server/index.html')