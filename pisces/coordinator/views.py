from bson import ObjectId
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import DateForm
from .models import *


class DateView(TemplateView):
    template_name = "coordinator/labs_list.html"

    def get(self, request):
        form = DateForm()
        return render(request, self.template_name, {"form": form, "title": 'Date'})


class LabListView(TemplateView):
    template_name = "coordinator/labs_list.html"
    all_labs = Labs.objects()
    all_labs_id = [ObjectId(i.id) for i in all_labs]
    all_labs_capacity = [i.capacity for i in all_labs]
    all_labs_room_no = [i.room_no for i in all_labs]
    all_time_slots = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    def get(self, request):
        print(request.GET["date"])
        result = Company.objects.filter(__raw__={"Test Date": "2019-08-05"})
        lab_time_slots = []
        for index in range(len(result)):
            r = Scheduling.objects.filter(__raw__={"_id": result[index].id})
            labs_taken = r[0].seating_information["labs"]
            lab_ids = [str(i) for i in labs_taken]
            time_slots = r[0].seating_information["time"]
            for j in range(len(self.all_labs_id)):
                if self.all_labs_id[j] not in lab_ids:
                    for slot in self.all_time_slots:
                        if slot not in time_slots:
                            lab_time_slots.append({'room_id': self.all_labs_room_no[j],
                                                   'time_slot': slot,
                                                   'capacity': self.all_labs_capacity[j]})
        print("slots:")
        print(lab_time_slots)
        return render(request, self.template_name, {'available': lab_time_slots})
