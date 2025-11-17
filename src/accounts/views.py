from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login realizado.')
            return redirect('common:home')
        messages.error(request, "Credenciais inválidas.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu.')
    return redirect('common:home')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        if username and password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                messages.success(request, 'Conta criada.')
                return redirect('common:home')
            messages.error(request, 'Nome de usuário já existe.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    return render(request, 'accounts/register.html')


def profile_view(request):
    return render(request, 'accounts/profile.html')
