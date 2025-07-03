from django.contrib import admin
from .models import Categoria, Forum, Topico, Postagem

admin.site.register(Categoria)
admin.site.register(Forum)
admin.site.register(Topico)
admin.site.register(Postagem)