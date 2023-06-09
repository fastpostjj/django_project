from random import sample

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import redirect

from config import settings
from user_auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView
from user_auth.forms import UserForm, UserRegisterForm


# Create your views here.

class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('user_auth:profile')

    def get_object(self, queryset=None):
        return self.request.user

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('products:index')
    template_name = 'user_auth/register.html'

    def form_valid(self, form):
        new_user = form.save()
        # send_mail(
        #     subject='Вы успешно зарегистрировались',
        #     message='Вы зарегистрировались. Добро пожаловать!',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[new_user.email]
        # )
        verification_kod = "".join(sample("".join([str(i) for i in range(0,10)]), 4))
        send_mail(
            subject='Вы начали процедуру регистрации',
            message=f'Вы начали процедуру регистрации на нашем сайте. Для завершения регистрации введите код:\n{verification_kod}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

def generate_new_password(request):
    password = "".join(sample("".join([str(i) for i in range(0,10)]) + "*+-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 10))
    request.user.set_password(password)
    request.user.save()
    send_mail(
        subject='Новый пароль',
        message=f'Вам установлен новый пароль:\n{password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('user_auth:login'))




