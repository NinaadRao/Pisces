# Create your views here.
from django.contrib import messages
from django.conf import settings
from mongoengine import *
from .models import *
from bson import ObjectId
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests

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


class ListLabs(APIView):
    api_name = "list_labs"

    def get(self, request):
        print(self.api_name)
        try:
            year, month, date = (int(x) for x in request.GET["date"].split('-'))
        except ValueError:
            print("date request unpacking error - not enough values")
            return Response({'message': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST)
        print(year)
        print(month)
        print(date)
        try:
            ans = datetime.date(year, month, date)
        except ValueError:
            print("value error datetime")
            return Response({'message': 'invalid date'}, status=status.HTTP_400_BAD_REQUEST)

        day = ans.strftime("%A")
        global_slots_info = Labs.objects.filter(__raw__={"Day": day})
        company_result = Company.objects.filter(__raw__={"Test Date": request.GET["date"]})
        free_slots = global_slots_info[0].free_slots

        lab_time_slot_pair_set = set()
        for free_slot in free_slots:
            time_slot = free_slot["time_slot"]
            free_labs = free_slot["free_labs"]
            for lab in free_labs:
                lab_time_slot_pair_set.add(lab + "," + time_slot)

        for index in range(len(company_result)):
            print("Index = " + str(index))
            scheduling_result = Scheduling.objects.filter(__raw__={"_id": company_result[index].id})
            if len(scheduling_result) == 0:
                continue
            labs_taken = scheduling_result[0].seating_information["labs"]
            lab_ids_taken = [str(i) for i in labs_taken]
            time_slots_taken = scheduling_result[0].seating_information["time"]
            for free_slot in free_slots:
                time_slot = free_slot["time_slot"]
                free_labs = free_slot["free_labs"]
                if time_slot in time_slots_taken:
                    for lab in free_labs:
                        if lab in lab_ids_taken:
                            lab_time_slot_pair_set.remove(lab + "," + time_slot)

        lab_time_slots = []
        for pair in lab_time_slot_pair_set:
            splits = pair.split(",")
            lab_time_slots.append({'room_id': splits[0],
                                   'time_slot': splits[1]})
        return Response({'available': lab_time_slots}, status=status.HTTP_200_OK)


class RemoveBooking(APIView):
    api_name = "update_booking"

    def post(self, request):
        print(self.api_name)
        # company_visit_id = request.POST("company_visit_id")
        company_visit_id = "5dc6eac7106ac20a0ef0543e"
        lab_numbers = []
        times = []
        Scheduling.objects(id=company_visit_id).update_one(
            set__seating_information={"time": times, "labs": lab_numbers})
        return Response({'message': 'Removed schedule for company'}, status=status.HTTP_200_OK)


class DisplayBooking(APIView):
    api_name = "display_booking"

    def get(self, request):
        print(self.api_name)
        # company_visit_id = request.POST("company_visit_id")
        company_visit_id = "5dc6eac7106ac20a0ef0543e"
        scheduling_result = Scheduling.objects.filter(__raw__={"_id": company_visit_id})

        if len(scheduling_result) == 0:
            return Response({'message': 'Company visit does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        labs_taken = scheduling_result[0].seating_information["labs"]
        lab_ids_taken = [str(i) for i in labs_taken]
        time_slots_taken = scheduling_result[0].seating_information["time"]

        return Response({'labs_taken': lab_ids_taken, 'time_slots_taken': time_slots_taken},
                        status=status.HTTP_200_OK)


class UpsertBooking(APIView):
    api_name = "upsert_booking"

    def post(self, request):
        print(self.api_name)
        # company_visit_id = request.POST("company_visit_id")
        company_visit_id = "5dc6eac7106ac20a0ef0543e"
        chosen_labs_field_value = request.POST["chosen_labs_field"]
        labs_chosen = chosen_labs_field_value.split(",")

        print(labs_chosen)

        if len(labs_chosen) % 2 != 0:
            return Response({'message': 'Error with input'}, status=status.HTTP_400_BAD_REQUEST)

        lab_numbers = []
        times = []

        i = 0
        while i < len(labs_chosen):
            lab_numbers.append(labs_chosen[i])
            times.append(labs_chosen[i + 1])
            i += 2

        print(Scheduling.objects(id=company_visit_id))
        Scheduling.objects(id=company_visit_id).update_one(
            set__seating_information={"time": times, "labs": lab_numbers})
        return Response({'message': "Added schedule for company"}, status=status.HTTP_200_OK)


class LabListView(TemplateView):
    template_name = "coordinator/labs_list_3.html"

    def get(self, request):
        print(self.template_name)
        params = {"date": request.GET["date"]}
        response = requests.get("http://0.0.0.0:8001/coordinator/list_labs",
                                params=params)
        if response.status_code != 200:
            return JsonResponse({'message': "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        lab_time_slots = response.json()["available"]
        book_form = BookForm()
        return render(request, self.template_name, {"available": lab_time_slots, "book_form": book_form})
