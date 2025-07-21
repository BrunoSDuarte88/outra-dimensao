from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re
from django.conf import settings

def validar_username_com_espaco(value):
    if not re.match(r'^[\w\s.@+-]+$', value):
        raise ValidationError('Nome de usuário pode conter apenas letras, números, espaços e @/./+/-/_ caracteres.')

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validar_username_com_espaco],
        error_messages={
            'unique': "Um usuário com esse nome já existe.",
        },
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "Um usuário com esse e-mail já existe.",
        },
    )

class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    nome_completo = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True, default='')

    instagram = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    facebook = models.URLField(blank=True, default='')
    youtube = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')

    # redes_sociais = models.TextField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    assinatura_url = models.URLField(blank=True, default='')

    TEMA_CHOICES = [
        ('claro', 'Claro'),
        ('escuro', 'Escuro'),
    ]
    tema = models.CharField(max_length=10, choices=TEMA_CHOICES, default='escuro')

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def save(self, *args, **kwargs):
        if self.telefone:
            # Remove qualquer caractere que não seja número
            self.telefone = re.sub(r'\D', '', self.telefone)
        super().save(*args, **kwargs)

from django.utils import timezone

class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = 'Solicitação de Amizade'
        verbose_name_plural = 'Solicitações de Amizade'

    def __str__(self):
        return f"Solicitação de {self.from_user.username} para {self.to_user.username}"

class Friendship(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendships_iniciadas', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendships_recebidas', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        verbose_name = 'Amizade'
        verbose_name_plural = 'Amizades'

    def __str__(self):
        return f"Amizade entre {self.user1.username} e {self.user2.username}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)  # Link para exibir detalhes
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificação para {self.user.username}: {self.message}"
