from django.shortcuts import render, get_object_or_404
from .models import Categoria, Forum, Topico, Postagem

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'forum/lista_categorias.html', {'categorias': categorias})

def lista_foruns(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    foruns = categoria.foruns.all()
    return render(request, 'forum/lista_foruns.html', {'categoria': categoria, 'foruns': foruns})

def lista_topicos(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    topicos = forum.topicos.order_by('-atualizado_em')
    return render(request, 'forum/lista_topicos.html', {'forum': forum, 'topicos': topicos})

def detalhe_topico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    postagens = topico.postagens.order_by('criado_em')
    return render(request, 'forum/detalhe_topico.html', {'topico': topico, 'postagens': postagens})

def responder_topico(request, topico_id):
    # esqueleto — deixaremos para quando criarmos os formulários
    pass
