from django.contrib.auth.forms import UserChangeForm
from user_auth.models import User
from django.urls import reverse_lazy
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



