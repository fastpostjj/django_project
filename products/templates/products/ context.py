from django.contrib.auth.models import User

def current_user(request):
    if request.user.is_authenticated:
        return {'current_user': request.user}
    else:
        return {}