# Custom
from waauth.models import WAUser

def waauth(request):
    wa_user = None
    try:
        if request.user.is_authenticated():
            # wa_user = WAUser.objects.get(user=request.user)
            # FIXME is this right?
            wa_user = request.user
    except WAUser.DoesNotExist:
        pass
    return { 'wa_user': wa_user }