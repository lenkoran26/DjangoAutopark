from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegistrationForm, ClientForm, LoginUserForm
from AutoparkProject.utils import calculate_age
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView
from .models import Client

def index(request):
    return render(request, 'users/index.html')

def register(request):
    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)
        client_form = ClientForm(request.POST)

        if reg_form.is_valid() and client_form.is_valid():
            user = reg_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.age = calculate_age(client.birthday)
            client.save()

            return register_done(request, new_user=client)

    # для метода GET
    reg_form = RegistrationForm()
    client_form = ClientForm()
    context = {"reg_form": reg_form, "client_form": client_form}

    return render(request, "users/register.html", context=context)


def register_done(request, new_user):
    context = {"client": new_user, "title": "Успешная регистрация"}
    return render(request, "users/register_done.html", context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    # form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('users:index')


class ProfileView(DetailView):
    model = Client
    template_name = 'users/profile.html'
    context_object_name = 'client'
