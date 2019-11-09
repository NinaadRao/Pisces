from bson import ObjectId
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import *
from .models import *

import datetime


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
