from django.contrib import messages
import cloudinary.uploader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from accounts.models import Profile


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

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar_file = request.FILES['avatar']

        try:
            # Upload para Cloudinary
            upload_result = cloudinary.uploader.upload(
                avatar_file,
                asset_folder='senacmon/avatars',
                public_id=f'user_{request.user.id}',
                overwrite=True,
                resource_type='image'
            )

            profile.avatar_url = upload_result['secure_url']
            profile.save()
            messages.success(request, 'Avatar atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao fazer upload do avatar: {str(e)}')

    return render(request, 'accounts/profile.html')
