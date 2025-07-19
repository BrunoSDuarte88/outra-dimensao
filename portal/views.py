from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required  # <- IMPORTANTE
from .models import Perfil
from .forms import CadastroForm, PerfilForm, EditarPerfilForm
from django.core.mail import send_mail
from django.conf import settings
import requests
import datetime

from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponse
from django.core.management import call_command
from forum.models import Postagem
from django.contrib.sessions.models import Session
from django.utils import timezone


User = get_user_model()

def portal_view(request):
    total_membros = User.objects.count()
    total_posts = Postagem.objects.count()
    online = contar_usuarios_online()
    try:
        ultimo_membro = User.objects.latest('date_joined')
    except User.DoesNotExist:
        ultimo_membro = None

    hoje = datetime.date.today()
    # Filtra perfis com aniversário hoje (mesmo dia e mês)
    aniversariantes_hoje = Perfil.objects.filter(
        data_nascimento__month=hoje.month,
        data_nascimento__day=hoje.day
    )

    return render(request, 'portal/portal.html', {
        'total_membros': total_membros,
        'total_posts': total_posts,
        'ultimo_membro': ultimo_membro,
        'aniversariantes_hoje': aniversariantes_hoje,
        'total_online': online['total_online'],
        'registrados_online': online['registrados_online'],
        'visitantes_online': online['visitantes_online'],
    })
    # return render(request, 'portal/portal.html')


def contar_usuarios_online():
    # Sessões não expiradas
    sessoes_ativas = Session.objects.filter(expire_date__gte=timezone.now())

    usuarios_online_ids = set()
    visitantes_online = 0

    for sessao in sessoes_ativas:
        data = sessao.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            usuarios_online_ids.add(user_id)
        else:
            visitantes_online += 1

    usuarios_online = User.objects.filter(id__in=usuarios_online_ids)

    return {
        'total_online': usuarios_online.count() + visitantes_online,
        'registrados_online': usuarios_online.count(),
        'visitantes_online': visitantes_online,
    }

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # Mantém espaços
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('portal')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'portal/portal.html')

def cadastro_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, 'Por favor, confirme que você não é um robô.')
            form = CadastroForm(request.POST)
            return render(request, 'portal/cadastro.html', {'form': form})

        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_mail(
                'Bem-vindo ao Outra Dimensão!',
                f'Olá {user.username}, seu cadastro foi realizado com sucesso!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect('cadastro_sucesso')
    else:
        form = CadastroForm()

    return render(request, 'portal/cadastro.html', {'form': form})


def cadastro_sucesso_view(request):
    return render(request, 'portal/cadastro_sucesso.html')

@login_required  # <- ESSENCIAL AQUI
def perfil_view(request):
    return render(request, 'portal/perfil.html')

@login_required  # <- ESSENCIAL AQUI
def editar_perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, user=user)
        if form.is_valid():
            # Atualiza username, email, perfil
            form.save(commit=True)

            # Se o usuário preencheu o campo senha atual, tenta alterar senha
            senha_atual = request.POST.get('senha_atual')
            nova_senha = request.POST.get('nova_senha')
            nova_senha_conf = request.POST.get('nova_senha_confirm')

            if senha_atual or nova_senha or nova_senha_conf:
                # Verifica se todos os campos estão preenchidos
                if not (senha_atual and nova_senha and nova_senha_conf):
                    messages.error(request, 'Para alterar a senha, preencha todos os campos de senha.')
                    return render(request, 'portal/editar_perfil.html', {'form': form})

                # Verifica se senha atual confere
                if not user.check_password(senha_atual):
                    messages.error(request, 'Senha atual incorreta.')
                    return render(request, 'portal/editar_perfil.html', {'form': form})

                # Verifica se nova senha e confirmação conferem
                if nova_senha != nova_senha_conf:
                    messages.error(request, 'A nova senha e a confirmação não conferem.')
                    return render(request, 'portal/editar_perfil.html', {'form': form})

                # Tudo certo, atualiza a senha
                user.set_password(nova_senha)
                user.save()
                # Atualiza a sessão para não deslogar o usuário
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')

        else:
            messages.error(request, 'Corrija os erros abaixo.')

    else:
        form = EditarPerfilForm(user=user)

    return render(request, 'portal/editar_perfil.html', {'form': form})

def atualizar_tema_view(request):
    if request.method == 'POST':
        novo_tema = request.POST.get('tema')
        if novo_tema in ['claro', 'escuro']:
            perfil = request.user.perfil
            perfil.tema = novo_tema
            perfil.save()
    return redirect('perfil')  # redireciona de volta à página do perfil

@user_passes_test(lambda u: u.is_superuser)
def acp_view(request):
    return render(request, 'portal/acp.html')

@user_passes_test(lambda u: u.is_superuser)
def gerenciar_usuarios_view(request):
    return render(request, 'portal/gerenciar_usuarios.html')
@user_passes_test(lambda u: u.is_superuser)
def gerenciar_grupos_view(request):
    return render(request, 'portal/gerenciar_grupos.html')

@user_passes_test(lambda u: u.is_superuser)
def gerenciar_categorias_view(request):
    return render(request, 'portal/gerenciar_categorias.html')

@user_passes_test(lambda u: u.is_superuser)
def gerenciar_posts_view(request):
    return render(request, 'portal/gerenciar_posts.html')


# def run_migrate(request):
#     call_command('migrate')
#     return HttpResponse("Migrações aplicadas com sucesso!")

