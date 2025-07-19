from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def usuarios_online(request):
    sessoes_ativas = Session.objects.filter(expire_date__gte=timezone.now())

    usuarios_online_ids = set()
    visitantes_online = 0

    for sessao in sessoes_ativas:
        data = sessao.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            usuarios_online_ids.add(user_id)
        else:
            visitantes_online += 1

    usuarios_online = User.objects.filter(id__in=usuarios_online_ids)

    return {
        'total_online': usuarios_online.count() + visitantes_online,
        'registrados_online': usuarios_online.count(),
        'visitantes_online': visitantes_online,
    }
