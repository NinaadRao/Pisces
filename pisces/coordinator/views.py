# Create your views here.
from django.contrib import messages
from django.conf import settings
from mongoengine import *
from .models import *
from bson import ObjectId
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from .models import *
import datetime
import os
from django.contrib.auth import authenticate, login, logout
from .forms import UsersLoginForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView
import re
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
                return render(request, 'coordinator/home.html', details)

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


class Search(TemplateView):
    template_name = 'coordinator/search.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        result = User.objects.filter(srn=request.POST["usn"])
        if len(result):
            details = {}
            for i in result[0]:
                details[i] = result[0][i]
            del details['id']
            del details['password']
            print(details)
            return JsonResponse(details)


class Company_list(TemplateView):
    template_name = 'coordinator/company.html'

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


class LabListView(TemplateView):
    template_name = "coordinator/labs_list.html"

    def get(self, request):
        year, month, date = (int(x) for x in "2019-08-05".split('-'))
        ans = datetime.date(year, month, date)
        day = ans.strftime("%A")
        global_slots_info = Labs.objects.filter(__raw__={"Day": day})
        result = Company.objects.filter(__raw__={"Test Date": "2019-08-05"})
        lab_time_slots = []
        free_slots = global_slots_info[0].free_slots
        for index in range(len(result)):
            r = Scheduling.objects.filter(__raw__={"_id": result[index].id})
            labs_taken = r[0].seating_information["labs"]
            lab_ids_taken = [str(i) for i in labs_taken]
            time_slots_taken = r[0].seating_information["time"]
            for free_slot in free_slots:
                time_slot = free_slot["time_slot"]
                free_labs = free_slot["free_labs"]
                if time_slot not in time_slots_taken:
                    for lab in free_labs:
                        if lab not in lab_ids_taken:
                            lab_time_slots.append({'room_id': lab,
                                                   "time_slot": time_slot})
        print("slots:")
        print(lab_time_slots)

        book_form = BookForm()

        return render(request, self.template_name, {'available': lab_time_slots, "book_form": book_form})

    def post(self, request):
        # company_visit_id = request.POST("company_visit_id")
        chosen_labs_field_value = request.POST["chosen_labs_field"]
        labs_chosen = chosen_labs_field_value.split(";")
        lab_numbers = []
        times = []
        for lab in labs_chosen:
            values = lab.split(",")
            lab_numbers.append(values[0])
            times.append(values[1])

        company_visit_id = "5da49c32106ac2329399c81a"

        print(Scheduling.objects(id=company_visit_id))
        Scheduling.objects(id=company_visit_id).update_one(set__seating_information={"time": times, "labs": lab_numbers})

        return render(request, self.template_name)
