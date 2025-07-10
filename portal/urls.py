from django.urls import path
from . import views  # importa tudo de views.py
from .views import editar_perfil_view
from django.contrib.auth.views import LogoutView
from .views import run_migrate  # rota de migração temporária (desativada por segurança)

urlpatterns = [
    path('', views.portal_view, name='portal'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('cadastro/sucesso/', views.cadastro_sucesso_view, name='cadastro_sucesso'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),
    path('atualizar-tema/', views.atualizar_tema_view, name='atualizar_tema'),

    path('run-migrate/', run_migrate, name='run_migrate'), # rota de migração temporária (desativada por segurança)
]