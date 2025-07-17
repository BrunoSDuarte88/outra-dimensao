from django.contrib import admin
from .models import Categoria, Forum, Topico, Postagem

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'descricao')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')

@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'forum', 'autor', 'criado_em', 'fechado')
    list_filter = ('forum', 'fechado')
    search_fields = ('titulo', 'autor__username')
    date_hierarchy = 'criado_em'

@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('autor', 'topico', 'criado_em')
    list_filter = ('topico',)
    search_fields = ('conteudo', 'autor__username')
    date_hierarchy = 'criado_em'
