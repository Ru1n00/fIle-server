from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.static import serve
from django.contrib import messages

from .models import File
from .forms import FileForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user)
        return render(request, 'file_server/index.html', {'files': files})
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
    

@login_required(login_url='file_server:login')
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.user = request.user
            file_obj.save()
            return redirect('file_server:index')
        else:
            msgs = form.errors
            for msg in msgs:
                message = msgs[msg][0]
            messages.info(request, message)
            return render(request, 'file_server/upload_file.html')

    return render(request, 'file_server/upload_file.html', {'form': FileForm()})


@login_required(login_url='file_server:login')
def delete_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
    except:
        message = 'File does not exist'
        messages.info(request, message)
        return redirect('file_server:index')
    if file.user == request.user:
        file.delete()
        return redirect('file_server:index')
    else:
        message = 'You are not authorized to delete this file'
        messages.info(request, message)
        return redirect('file_server:index')


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('file_server:index')
        else:
            message = 'Invalid username or password'
            messages.info(request, message)
            return render(request, 'file_server/sign_in.html')
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('file_server:index')
        return render(request, 'file_server/sign_in.html')
    # return render(request, 'file_server/sign_in.html')


def sign_up(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # save user
            user = form.save()
            # login user
            login(request, user)
            return redirect('file_server:index')
        else:
            msgs = form.errors
            for msg in msgs:
                message = msgs[msg][0]
                print(message, type(message))
            # messages.info(request, message)
            return render(request, 'file_server/sign_up.html', {'form': form})
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('file_server:index')
        return render(request, 'file_server/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('file_server:index')
    # return render(request, 'file_server/index.html')