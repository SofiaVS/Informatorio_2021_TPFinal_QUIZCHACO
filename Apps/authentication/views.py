from django.shortcuts import render, redirect
from .forms import RegisterForm, UsuarioLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

# login
def Login(request):
    titulo = 'Login'
    form = UsuarioLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect('home')

    context = {
        'form': form,
        'titulo': titulo
    }

    return render(request, 'auth/login.html', context)

# Register


def Register(request):
    titulo = 'Crea una cuenta'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(
                request, f'Usuario {username} creado correctamente.')
            form.save()
            # return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'titulo': titulo,
    }
    return render(request, 'auth/register.html', context)


def Logout(request):
    logout(request)
    return redirect('/')
