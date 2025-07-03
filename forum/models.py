from django.db import models
from django.conf import settings  # ✅ Importa o modelo de usuário customizado

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da categoria do fórum")
    descricao = models.TextField(blank=True, help_text="Descrição breve da categoria")

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class Forum(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='foruns')
    nome = models.CharField(max_length=100, help_text="Nome do fórum")
    descricao = models.TextField(blank=True, help_text="Descrição breve do fórum")

    def __str__(self):
        return f"{self.nome} (Categoria: {self.categoria.nome})"

class Topico(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topicos')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topicos')  # ✅ Corrigido
    titulo = models.CharField(max_length=200)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    fechado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Postagem(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, related_name='postagens')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='postagens')  # ✅ Corrigido
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post de {self.autor.username} em {self.topico.titulo}"
