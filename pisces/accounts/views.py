from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UsersRegisterForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
# Create your views here.
from mongoengine import *
from .models import *


class login(TemplateView):
    template_name = 'accounts/form.html'

    def get(self, request):
        form = UsersLoginForm()
        return render(request, self.template_name, {"form": form, "title": 'Login'})

    def post(self, request):
        form = UsersLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username, password)
            query = {'srn': username, 'password': password}
            result = User.objects.filter(srn=username, password=password)
            print(len(result))
            # print(result)

            form = UsersLoginForm()
            # print(type(result),result.objects)

            if len(result):
                # request.session['username'] = username
                return render(request, 'success.html', {"form": form})
            return render(request, self.template_name, {"form": form, "title": 'Login'})


'''def login_view(request):
    form = UsersLoginForm(request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        #user = authenticate(username = username, password = password)
        #login(request, user)
        return redirect("/")
    return render(request, "accounts/form.html", {
        "form" : form,
        "title" : "Login",
    })


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect("/accounts/login")
    return render(request, "accounts/form.html", {
        "title" : "Register",
        "form" : form,
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")'''
