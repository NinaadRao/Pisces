from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UserUpdatePassword
from django.http import HttpResponseRedirect, HttpResponse
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
                if username == "admin":
                    request.session['username'] = username
                    details = {}
                    for i in result[0]:
                        details[i]=result[0][i]
                    print(details)
                    details['form'] = form
                    del details['password']
                    del details['id']
                    return redirect('/coordinator/homepage')
                else:
                    request.session['username'] = username
                    details = {}
                    for i in result[0]:
                        details[i] = result[0][i]
                    print(details)
                    details['form'] = form
                    del details['password']
                    del details['id']
                    details['gender'] = str(details['gender']).lower()
                    return redirect('/students/homepage')
            return render(request, self.template_name, {"form": form, "title": 'Login'})


class logout(TemplateView):
    template_name = 'accounts/form.html'

    def get(self, request):
        if 'username' in request.session:
            del request.session['username']
            form = UsersLoginForm()
            return redirect('/accounts/login')
        else:
            return HttpResponse(status=400)

    def post(self, request):
        return HttpResponse(status=400)


class updatePassword(TemplateView):
    template_name = 'accounts/updatePassword.html'

    def get(self, request):
        if 'username' in request.session:
            form = UserUpdatePassword()
            return render(request, self.template_name,
                          {'form': form, 'title': 'Change Password', 'user': request.session['username']})

    def post(self, request):
        form = UserUpdatePassword(request.POST)
        if form.is_valid():
            if 'username' in request.session:
                password = form.cleaned_data.get("newPassword")
                oldPassword = form.cleaned_data.get('oldPassword')
                actualPassword = (User.objects.get(srn=request.session['username'])).password
                print('passwords', actualPassword, password, oldPassword)
                if actualPassword == oldPassword:
                    print('new', password)
                    updatePasswordObject = User.objects.get(srn=request.session['username'])
                    updatePasswordObject.update(set__password=password)
                    print(updatePasswordObject.password)

                    updatePasswordObject.save()
                    print(request.session)
                    del request.session['username']
                    # del request.session['password']
                    return redirect("/accounts/login")
                else:
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)
        return HttpResponse(status=400)


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
