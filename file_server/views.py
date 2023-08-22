from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import File

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user)
        return render(request, 'file_server/index.html', {'files': files})
    return render(request, 'file_server/index.html')

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login user
            login(request, user)
            return redirect('file_server:index')
        else:
            return render(request, 'file_server/sign_in.html', {'error': 'Invalid username or password'})
        
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'file_server/sign_in.html', {'form': form})
    # return render(request, 'file_server/sign_in.html')

def sign_out(request):
    logout(request)
    return redirect('file_server:index')
    # return render(request, 'file_server/index.html')