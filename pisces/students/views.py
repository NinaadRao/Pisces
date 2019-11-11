# Create your views here.
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm, UserUpdatePassword
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
import re
# Create your views here.
from django.contrib import messages
from django.conf import settings
from mongoengine import *
from .models import *
import json
from django.core.files.storage import FileSystemStorage


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
                return render(request, 'home.html', details)

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
        return render(request,self.template_name,{'details':details,'notRendered':["_id","id",]})


class register(TemplateView):
    job_stat=dict()
    job_stat["Full Time Employment + Internship (Mandatory)"]=4
    job_stat["Internship only"] = 1
    job_stat["Full Time Employment only"] = 3
    job_stat["Full Time Employment + Internship"] = 4
    job_stat["Only if 4th years available for minimum 4-6 months internship"] = 1
    success = 'registered.html'
    failure = 'icant.html'
    already = 'already.html'
    def get(self,request):
        print('Good Job',request.GET)

        if 'companyId' in request.GET and 'username' in request.session:
            print('check')
            print(request.GET['companyId'])
            id = request.GET['companyId']
            result = Company.objects.get(id=id)
            #print(result["Test Date"],request.session['username'])
            userDetails = User.objects.get(srn=request.session['username'])

            # Status for user 0-nothing, 1-internship , 2-tier2, 3-fte only 4-fte+internship
            print(result['Criteria'],result['Job Status'])
            # 1- internship, 3-fte only 4- fte+internship
            jobStatusAvailable = []
            for i in result['Job Status']:
                jobStatusAvailable.append(self.job_stat[i])
            print(float(userDetails['cgpa'])>=float(result['Criteria']['BE']['CGPA']))
            print((result['Criteria']['12th']))

            if float(userDetails['cgpa'])>=float(result['Criteria']['BE']['CGPA'])  and (result['Criteria']['12th']==None or float(userDetails['twelfth'])>=float(re.search(r"\d+\.?\d+", result['Criteria']['12th']).group())) and (result['Criteria']['10th']==None or float(userDetails['tenth'])>=float(re.search(r"\d+\.?\d+", result['Criteria']['10th']).group())):
                currentStatus = int(userDetails['status'])
                print('Status is',currentStatus)
                if(currentStatus==5):
                    # he already has two offers. not allowed anymore
                    print("cannot register")
                    return render(request,self.failure)
                elif(currentStatus==0):
                    # means he can definitely register
                    print('Can definitely register')
                    print(str(userDetails['id']),type(userDetails['id']))
                    checking = scheduling_information.objects.get(id = id)
                    #print(type(checking["student_list"]))
                    if(userDetails['id'] not in set(checking['student_list'])):
                        company_name = scheduling_information.objects.get(id = id)
                        company_name.save()
                        company_name.update(push__student_list=userDetails["id"])
                        company_name.save()
                        return render(request,'registered.html')
                    # already_registered
                    print("you have already registered")
                    return render(request,'already.html',{})
                elif(currentStatus==1):
                    # means he has an internship and only if it is a fte only, he can register
                    print('means he has an internship and only if it is a fte only, he can register')
                    if(3 in jobStatusAvailable):
                        checking = scheduling_information.objects.get(id=id)
                        # print(type(checking["student_list"]))
                        if (userDetails['id'] not in set(checking['student_list'])):
                            company_name = scheduling_information.objects.get(id=id)
                            company_name.save()
                            company_name.update(push__student_list=userDetails)
                            company_name.save()
                            print("Registered")
                            return render(request,'registered.html')
                        # already_registered
                        print('Already registered',currentStatus)
                        return render(request,'home.html')
                    else:
                        # not allowed to register
                        print("Not allowed to register")
                        return render(request,'icant.html')
                elif(currentStatus==2):
                    #he has tier-2.
                    # he can register
                    print("can register status:",currentStatus)
                    checking = scheduling_information.objects.get(id=id)
                    # print(type(checking["student_list"]))
                    if (userDetails['id'] not in set(checking['student_list'])):
                        company_name = scheduling_information.objects.get(id=id)
                        company_name.save()
                        company_name.update(push__student_list=userDetails)
                        company_name.save()
                        print("Registered")
                        return render(request,'registered.html')
                    # already_registered
                    print('Already registered', currentStatus)
                    return render(request,'already.html')
                elif(currentStatus==3):
                    # he has fte. can do only internship
                    print("he has fte. can do only internship")
                    if(1 in jobStatusAvailable):
                        #allow registration
                        checking = scheduling_information.objects.get(id=id)
                        # print(type(checking["student_list"]))
                        print('allowed')
                        if (userDetails['id'] not in set(checking['student_list'])):
                            company_name = scheduling_information.objects.get(id=id)
                            company_name.save()
                            company_name.update(push__student_list=userDetails)
                            company_name.save()
                            print(successful)
                            return render(request,'registered.html')
                        # already_registered
                        print("already registered")
                        return render(request,'already.html')
                    else:
                        # not allowed to register
                        print('not allowed to register')
                        return render(request,'icant.html')
                elif(currentStatus==4):
                    # Not allowed to register
                    print("not allowed to register",currentStatus)
                    return render(request,'icant.html')

            else:
                # Not meeting eligibility criteria
                return HttpResponse(status=200)
            return HttpResponse(status=200)

        return HttpResponse(status=400)


class uploadResume(TemplateView):
    def post(self,request):
        uploaded_file = request.FILES['resume']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        if('pdf' in uploaded_file.name or 'doc' in uploaded_file.name):
            files=set(os.listdir(settings.MEDIA_ROOT))
            print(files)
            for i in files:
                if request.session['username'] in i:
                    os.remove(settings.MEDIA_ROOT+'/'+i)
            fileName = request.session['username']+'.'+uploaded_file.name.split('.')[-1]
            fs.save(fileName,uploaded_file)
            userUpload=User.objects.get(srn=request.session['username'])
            userUpload.update(set__file=fileName)
            return redirect('/students/homepage')
        else:
            messages.info(request, 'File not uploaded')
            return redirect('/students/homepage')
