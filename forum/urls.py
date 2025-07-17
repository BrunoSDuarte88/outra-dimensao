# forum/urls.py
from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('categoria/<int:categoria_id>/', views.lista_foruns, name='lista_foruns'),
    path('forum/<int:forum_id>/', views.lista_topicos, name='lista_topicos'),
    path('topico/<int:topico_id>/', views.detalhe_topico, name='detalhe_topico'),
    path('topico/<int:topico_id>/responder/', views.responder_topico, name='responder_topico'),
]
