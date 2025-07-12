from django import template

register = template.Library()

@register.filter
def format_telefone(value):
    """
    Formata número tipo 5511999999999 para +55 (11) 99999-9999
    """
    if not value or len(value) < 12:
        return value  # Se for inválido ou muito curto, retorna como está
    ddd = value[2:4]
    numero = value[4:]
    return f'+{value[:2]} ({ddd}) {numero[:5]}-{numero[5:]}'
