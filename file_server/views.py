from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
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
            return render(request, 'file_server/index.html')
        else:
            return render(request, 'file_server/sign_in.html', {'error': 'Invalid username or password'})
        
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'file_server/sign_in.html', {'form': form})
    # return render(request, 'file_server/sign_in.html')

def sign_out(request):
    logout(request)
    return render(request, 'file_server/index.html')