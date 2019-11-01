from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UserUpdatePassword
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
# Create your views here.
from mongoengine import *
from .models import *
import json


class HomePage(TemplateView):
    def get(self,request):
        if 'username' in request.session:
            result = User.objects.filter(srn=request.session['username'])
            if len(result):

                details = {}
                for i in result[0]:
                    details[i]=result[0][i]
                print(details)

                del details['password']
                del details['id']
                details['gender']= str(details['gender']).lower()
                return render(request, 'home_user.html', details)

        else:
            return redirect('/accounts/login')

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
    template_name = 'updatePassword.html'

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

class Company_list(TemplateView):
    template_name = 'company.html'
    def get(self, request):

        companies = Company.objects.filter()
        details = json.loads(companies.to_json())
        #print(details)
        for i in range(len(details)):
            details[i]['Compensation'] = dict(details[i]['Compensation'])
            print(details[i]['_id'],type(details[i]['_id']))
            details[i]['id'] = details[i]['_id']['$oid']
            #print(type(details[i]['Compensation']))
        return render(request,self.template_name,{'details':details})
