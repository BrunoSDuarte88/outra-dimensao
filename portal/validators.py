import re
from django.core.exceptions import ValidationError

def validar_username_com_espaco(username):
    # Verifica se começa ou termina com espaço
    if username != username.strip():
        raise ValidationError("O nome de usuário não pode começar ou terminar com espaço.")

    # Verifica se contém apenas caracteres válidos: letras, números, espaço, @ . + - _
    if not re.match(r'^[\w\s.@+-]+$', username):
        raise ValidationError(
            'Use apenas letras, números, espaços (no meio) e os caracteres @/./+/-/_',
            code='invalid',
        )
