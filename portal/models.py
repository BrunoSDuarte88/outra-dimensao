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
    telefone = models.CharField(max_length=20, blank=True)
    redes_sociais = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    assinatura_url = models.URLField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
