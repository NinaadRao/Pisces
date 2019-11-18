# Create your views here.
import os
import datetime

import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response

from .forms import UsersLoginForm, UserUpdatePassword, SearchForm
from .forms import UsersLoginForm, UserUpdatePassword, BlogPost
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import TemplateView
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from keras.models import load_model
import keras
import numpy as np
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import json

from plotly.subplots import make_subplots
from collections import Counter
# Create your views here.
import io
import base64
import pandas as pd
from django.contrib import messages
from django.conf import settings
from mongoengine import *
from .models import *
import json
import pandas as pd
import os
import plotly.graph_objs as go
import plotly
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
import spacy

import pickle


class HomePage(TemplateView):
    def get(self, request):
        if 'username' in request.session:
            result = User.objects.filter(srn=request.session['username'])
            if len(result):

                details = {}
                for i in result[0]:
                    details[i] = result[0][i]
                print(details)

                del details['password']
                del details['id']
                details['gender'] = str(details['gender']).lower()
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
        return HttpResponse(status=403)


class updatePassword(TemplateView):
    template_name = 'updatePassword.html'

    def get(self, request):
        if 'username' in request.session:
            form = UserUpdatePassword()
            return render(request, self.template_name,
                          {'form': form, 'title': 'Change Password', 'user': request.session['username']})

    def post(self, request):
        form = UserUpdatePassword(request.POST)
        print('entered here')
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
        if('username' in request.session):
            t = datetime.date(datetime.now())

            print(type(t))
            companies = Company.objects.filter()
            print('This is the registration Deadline', type(companies[1]['Registration Deadline']),
                  companies[1]['Registration Deadline'])

            details = json.loads(companies.to_json())
            df = pd.DataFrame(details)

            df = df[df['Registration Deadline'] != '']
            deadlines = list(df['Registration Deadline'])
            deadlines = [i.split('T')[0] for i in deadlines]
            deadlines = [datetime.strptime(i, "%Y-%m-%d") for i in deadlines]
            df['Registration Deadline'] = deadlines

            df['Registration Deadline'] = pd.to_datetime(df['Registration Deadline'], format='%Y-%m-%d')
            print(df['Registration Deadline'][1], pd.Timestamp(t), df['Registration Deadline'][1] > pd.Timestamp(t))
            df = df.sort_values(by="Registration Deadline",ascending = False)
            details = list(df.T.to_dict().values())
            flag = 0
            flag2 = 0
            for i in range(len(details)):
                details[i]['Compensation'] = dict(details[i]['Compensation'])

                # print(details[i]['_id'],type(details[i]['_id']))
                details[i]['id'] = details[i]['_id']['$oid']
                if details[i]['Registration Deadline'] >= pd.Timestamp(t):
                    details[i]['allowed']=1
                else:
                    if(flag ==0):
                        flag=1
                        details[i]['first'] = 1
                    details[i]['allowed']=0
                # print(type(details[i]['Compensation']))
            return render(request, self.template_name, {'details': details, 'notRendered': ["_id", "id", ]})
        else:
            return redirect('/accounts/login')


class register(TemplateView):
    job_stat = dict()
    job_stat["Full Time Employment + Internship (Mandatory)"] = 4
    job_stat["Internship only"] = 1
    job_stat["Full Time Employment only"] = 3
    job_stat["Full Time Employment + Internship"] = 4
    job_stat["Only if 4th years available for minimum 4-6 months internship"] = 1
    success = 'registered.html'
    failure = 'icant.html'
    already = 'already.html'

    def get(self, request):
        print('Good Job', request.GET)

        if 'companyId' in request.GET and 'username' in request.session:
            print('check')
            print(request.GET['companyId'])
            id = request.GET['companyId']
            result = Company.objects.get(id=id)
            # print(result["Test Date"],request.session['username'])
            userDetails = User.objects.get(srn=request.session['username'])

            # Status for user 0-nothing, 1-internship , 2-tier2, 3-fte only 4-fte+internship
            print(result['Criteria'], result['Job Status'])
            # 1- internship, 3-fte only 4- fte+internship
            jobStatusAvailable = []
            for i in result['Job Status']:
                jobStatusAvailable.append(self.job_stat[i])
            print(float(userDetails['cgpa']) >= float(result['Criteria']['BE']['CGPA']))
            print((result['Criteria']['12th']))

            if float(userDetails['cgpa']) >= float(result['Criteria']['BE']['CGPA']) and (
                    result['Criteria']['12th'] == None or float(userDetails['twelfth']) >= float(
                re.search(r"\d+\.?\d+", result['Criteria']['12th']).group())) and (
                    result['Criteria']['10th'] == None or float(userDetails['tenth']) >= float(
                re.search(r"\d+\.?\d+", result['Criteria']['10th']).group())):
                currentStatus = int(userDetails['status'])
                print('Status is', currentStatus)
                if (currentStatus == 5):
                    # he already has two offers. not allowed anymore
                    print("cannot register")
                    return render(request, self.failure)
                elif (currentStatus == 0):
                    # means he can definitely register
                    print('Can definitely register')
                    print(str(userDetails['id']), type(userDetails['id']))
                    checking = scheduling_information.objects.get(id=id)
                    # print(type(checking["student_list"]))
                    if (userDetails['id'] not in set(checking['student_list'])):
                        company_name = scheduling_information.objects.get(id=id)
                        company_name.save()
                        company_name.update(push__student_list=userDetails["id"])
                        company_name.save()
                        return render(request, 'registered.html')
                    # already_registered
                    print("you have already registered")
                    return render(request, 'already.html', {})
                elif (currentStatus == 1):
                    # means he has an internship and only if it is a fte only, he can register
                    print('means he has an internship and only if it is a fte only, he can register')
                    if (3 in jobStatusAvailable):
                        checking = scheduling_information.objects.get(id=id)
                        # print(type(checking["student_list"]))
                        if (userDetails['id'] not in set(checking['student_list'])):
                            company_name = scheduling_information.objects.get(id=id)
                            company_name.save()
                            company_name.update(push__student_list=userDetails)
                            company_name.save()
                            print("Registered")
                            return render(request, 'registered.html')
                        # already_registered
                        print('Already registered', currentStatus)
                        return render(request, 'home.html')
                    else:
                        # not allowed to register
                        print("Not allowed to register")
                        return render(request, 'icant.html')
                elif (currentStatus == 2):
                    # he has tier-2.
                    # he can register
                    print("can register status:", currentStatus)
                    checking = scheduling_information.objects.get(id=id)
                    # print(type(checking["student_list"]))
                    if (userDetails['id'] not in set(checking['student_list'])):
                        company_name = scheduling_information.objects.get(id=id)
                        company_name.save()
                        company_name.update(push__student_list=userDetails)
                        company_name.save()
                        print("Registered")
                        return render(request, 'registered.html')
                    # already_registered
                    print('Already registered', currentStatus)
                    return render(request, 'already.html')
                elif (currentStatus == 3):
                    # he has fte. can do only internship
                    print("he has fte. can do only internship")
                    if (1 in jobStatusAvailable):
                        # allow registration
                        checking = scheduling_information.objects.get(id=id)
                        # print(type(checking["student_list"]))
                        print('allowed')
                        if userDetails['id'] not in set(checking['student_list']):
                            company_name = scheduling_information.objects.get(id=id)
                            company_name.save()
                            company_name.update(push__student_list=userDetails)
                            company_name.save()
                            print('successful')
                            return render(request, 'registered.html')
                        # already_registered
                        print("already registered")
                        return render(request, 'already.html')
                    else:
                        # not allowed to register
                        print('not allowed to register')
                        return render(request, 'icant.html')
                elif currentStatus == 4:
                    # Not allowed to register
                    print("not allowed to register", currentStatus)
                    return render(request, 'icant.html')

            else:
                # Not meeting eligibility criteria
                return render(request, 'icant.html')
            return render(request, 'icant.html')

        return redirect('/accounts/login')


class uploadResume(TemplateView):
    def post(self, request):
        if('username' in request.session):
            uploaded_file = request.FILES['resume']
            print(uploaded_file.name)
            print(uploaded_file.size)
            fs = FileSystemStorage()
            if ('pdf' in uploaded_file.name or 'doc' in uploaded_file.name):
                files = set(os.listdir(settings.MEDIA_ROOT))
                print(files)
                for i in files:
                    if request.session['username'] in i:
                        os.remove(settings.MEDIA_ROOT + '/' + i)
                fileName = request.session['username'] + '.' + uploaded_file.name.split('.')[-1]
                fs.save(fileName, uploaded_file)
                userUpload = User.objects.get(srn=request.session['username'])
                userUpload.update(set__file=fileName)
                return redirect('/students/homepage')
            else:
                messages.info(request, 'File not uploaded')
                return redirect('/students/homepage')
        else:
            redirect('accounts/login')


class viewSchedule(TemplateView):
    template_name = 'schedule.html'
    def get(self,request):
        if 'username' in request.session:
            t = datetime.date(datetime.now())
            user = User.objects.get(srn=request.session['username'])
            # user['id']
            companies = Company.objects.filter()
            # print(companies)
            print('This is the registration Deadline', type(companies[1]['Registration Deadline']),
                  companies[1]['Registration Deadline'])

            details = json.loads(companies.to_json())
            df = pd.DataFrame(details)
            # print(df.columns)

            # print(details)
            # df = df.dropna(subset=['Registration Deadline'])

            df = df[df['Registration Deadline'] != '']
            deadlines = list(df['Registration Deadline'])
            deadlines = [i.split('T')[0] for i in deadlines]
            deadlines = [datetime.strptime(i, "%Y-%m-%d") for i in deadlines]
            df['Registration Deadline'] = deadlines

            df['Registration Deadline'] = pd.to_datetime(df['Registration Deadline'], format='%Y-%m-%d')
            print(df['Registration Deadline'][1], pd.Timestamp(t), df['Registration Deadline'][1] > pd.Timestamp(t))
            df = df[df['Registration Deadline'] >= pd.Timestamp(t)]
            df = df.sort_values(by="Registration Deadline")
            details = list(df.T.to_dict().values())
            print(details[0])
            for i in range(len(details)):
                sched = scheduling_information.objects.get(id=details[i]['_id']['$oid'])
                print(type(details[i]),len(sched['student_list']),sched['id'])
                if(user['id'] in set(sched['student_list'])):
                    details[i]['room-no']=list(sched['seating_information']['labs'])[int(list(sched['student_list']).index(user['id'])//(len(list(sched['student_list']))/len(list(sched['seating_information']['time']))))]
                    print(details[i]['room-no'])
                    details[i]['time']=sched['seating_information']['time'][0]
                    print(details[i]['time'])
                else:
                   details[i] = ''
            while '' in details:
                details.remove('')
                #print(type(sched['student_list']),sched['student_list'])
            return render(request, self.template_name, {'details': details, 'notRendered': ["_id", "id", ]})
        else:
            return redirect('/accounts/login')


class Blog(TemplateView):
    template_name = 'blog-posts.html'

    def get(self,request):
        if('username' in request.session):
            form = BlogPost()
            blogs = blogging.objects.filter().order_by('-created_on')

            # print(blogs.to_json())
            #print(blogs[0].updated_on)
            blogs = json.loads(blogs.to_json())
            blogs = blogs[::-1]
            for i in blogs:
                # print(i['author'])
                i['author']=User.objects.get(id=i['author']['$oid'])['name']
                del i['content']
            print(len(blogs))
            return render(request, self.template_name, {"form": form,"blogs":blogs})
        else:
            return redirect('/accounts/login')
    def post(self,request):
        if('username' in request.session):
            print(request.POST)
            user = User.objects.get(srn=request.session['username'])
            content = dict()
            values = dict(request.POST)
            del values['csrfmiddlewaretoken']
            del values['blogTitle']
            del values['company']
            del values['blogType']
            del values['shortDescription']
            content = dict()
            for i in values:
                if('type' in i):
                    count = i.split('type')[1]
                    if(count not in content):
                        content[count] = ['','']
                    content[count][0]=values[i]
                elif('text' in i):
                    count = i.split('text')[1]
                    if(count not in content):
                        content[count]=['','']
                    content[count][1] = values[i]
            print(content)
            keys = list(content.keys())
            keys.sort()
            finalContent = []
            for i in keys:
                finalContent.append(content[i])
            newBlog = blogging()
            newBlog.title = request.POST['blogTitle']
            newBlog.author = user['id']
            newBlog.company = request.POST['company']
            newBlog.blogType = request.POST['blogType']
            newBlog.shortDescription = request.POST['shortDescription']
            newBlog.content = finalContent
            newBlog.save(force_insert=True)
            return redirect('/students/blog')
        else:
            return redirect('/accounts/login')


class SearchBlog(TemplateView):
    template_name = 'blog-posts.html'

    def get(self,request):
        return HttpResponse(status=403)

    def post(self,request):
        if('username' in request.session):
            form = BlogPost()
            blogs = blogging.objects.filter( Q(company__contains=request.POST['company']) |  Q(title__contains=request.POST['company']) | Q(shortDescription__contains=request.POST['company'])).order_by('-created_on')

            # print(blogs.to_json())
            # print(blogs[0].updated_on)
            blogs = json.loads(blogs.to_json())
            blogs = blogs[::-1]
            for i in blogs:
                # print(i['author'])
                i['author'] = User.objects.get(id=i['author']['$oid'])['name']
                del i['content']
            print(len(blogs))
            return render(request, self.template_name, {"form": form, "blogs": blogs})
        else:
            return redirect('/accounts/login')


class BlogDetails(TemplateView):
    template_name = 'blog-detail.html'
    def post(self,request):
        if('username' in request.session):
            print(request.POST)
            form = BlogPost()
            blog = blogging.objects.get(id=request.POST['id'])
            blog['author'] = User.objects.get(id=blog['author'])['name']
            blog = json.loads(blog.to_json())
            blog['content'] = list(blog['content'])
            del blog['_id']
            return render(request,self.template_name,{'blog':blog,'form':form})
        else:
            return redirect('/accounts/login')


def ctc(df):
    print(df.columns)
    dates = list(df['Date that the company has come'])
    dates = [datetime.strptime(i, "%Y-%m-%d") for i in dates]
    df['Date that the company has come'] = dates
    df = df.sort_values(by='Date that the company has come')
    trace1 = go.Scatter(x=df['Date that the company has come'], y=df['CTC'], mode='lines+markers',
                        hovertext=df['Name of company visited'],
                        marker=dict(
                            color='blue'
                        ))
    data = [trace1]
    layout = dict(
        title='CTC of companies over time',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )
    fig = dict(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots = [fig]

    ctc = df['CTC']
    dates = df['Date that the company has come']
    tier = dict(Counter(df['Tier']))
    data = [go.Bar(x=list(tier.keys()), y=list(tier.values()))]
    layout = dict(title='Tier based division of companies', xaxis=dict(title="Tier"),
                  yaxis=dict(title="Number of companies"))
    fig = go.Figure(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots += [fig]

    fig = make_subplots(rows=3, cols=2, subplot_titles=('July', "August", "September", "October", "November"))
    current = 1
    current_col = 1
    for i in range(8, 13):
        modified = df[(df['Date that the company has come'] < datetime.strptime("2019-" + str(i) + "-01","%Y-%m-%d")) & (df['Date that the company has come'] > datetime.strptime("2019-" + str(i - 1) + "-01", "%Y-%m-%d"))]
        # print('modified',modified)
        if (len(modified)):
            tier = dict(Counter(modified['Tier']))
            # print(current,current_col)
            fig.add_trace(go.Bar(x=list(tier.keys()), y=list(tier.values()), hovertext=list(tier.values())),
                          row=current, col=current_col)
            current_col += 1
            # print(current,current_col)
            if (current_col == 3):
                current_col = 1
                current += 1
    fig.update_layout(showlegend=False, height=1000, width=800, title="Tier division for different months")

    fig.update_yaxes(title_text="Number of companies", row=1, col=1)
    fig.update_yaxes(title_text="Number of companies", row=1, col=2)
    fig.update_yaxes(title_text="Number of companies", row=2, col=1)
    fig.update_yaxes(title_text="Number of companies", row=2, col=2)
    fig.update_yaxes(title_text="Number of companies", row=3, col=1)

    fig.update_xaxes(title_text="Tier", row=1, col=1)
    fig.update_xaxes(title_text="Tier", row=1, col=2)
    fig.update_xaxes(title_text="Tier", row=2, col=1)
    fig.update_xaxes(title_text="Tier", row=2, col=2)
    fig.update_xaxes(title_text="Tier", row=3, col=1)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots += [fig]

    counts = (Counter(df['category']))
    del counts['Others']
    a = counts.most_common()
    x_value = []
    y_value = []
    for i in a:
        x_value.append(i[0])
        y_value.append(i[1])
    print(a)
    data = [go.Bar(x=x_value, y=y_value)]
    layout = dict(title='Different Company categories', xaxis=dict(title="Company categories"),
                  yaxis=dict(title="Number of companies"))
    fig = go.Figure(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots+=[fig]

    values = []
    for i in range(8, 13):
        modified = df[(df['Date that the company has come'] < datetime.strptime("2019-" + str(i) + "-01",
                                                                                         "%Y-%m-%d")) & (df['Date that the company has come'] > datetime.strptime("2019-" + str(i - 1) + "-01", "%Y-%m-%d"))]
        # print('modified',modified)
        if (len(modified)):
            tier = sum(modified['number'])
            values.append(tier)

    data = [go.Bar(x=['July', 'August', 'September', 'October', 'November'], y=values)]
    layout = dict(title='How many students are placed?', xaxis=dict(title="Month"),
                  yaxis=dict(title="Number of students"))
    fig = go.Figure(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots += [fig]

    values = []
    for i in range(1, 4):
        modified = df[df['Tier'] == i]
        values.append(sum(modified['number']))

    data = [go.Bar(x=['Tier-1', 'Tier-2', 'Tier-3'], y=values)]
    layout = dict(title='Students composition based on company tiers', xaxis=dict(title="Month"),
                  yaxis=dict(title="Number of students"))
    fig = go.Figure(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots += [fig]

    data = [go.Box(x=df['CTC'], name='CTC offered', boxmean=True)]
    layout = dict(title='CTC summary', xaxis=dict(title='CTC'))
    fig = go.Figure(data=data, layout=layout)
    fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    plots += [fig]

    return plots


def wordCloud(df):
    d = {}
    for i in range(len(df)):
        d[df['Name of company visited'][i]] = float(df["CTC"][i].replace(',', ''))

    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=d)

    plt.figure(figsize=(10, 10), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Companies that visited in 2019')


    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)




class ViewStatistics(TemplateView):
    template_name = 'stats.html'
    df = pd.read_csv("detail.csv")
    df = df.sort_values(by='Date that the company has come')
    df = df.reset_index(drop=True)
    a = list(df['CTC'])
    print(len(a))
    first = float(a[-1].replace(',', ''))
    first = first / 100000
    second = float(a[-2].replace(',', ''))
    second = second / 100000
    to_be_predicted = np.array([[second, first]])
    to_be_predicted = to_be_predicted.reshape(to_be_predicted.shape[0], to_be_predicted.shape[1], 1)
    model = load_model('ctc_lstm.h5')
    value = model.predict(to_be_predicted, verbose=0)
    print('This is the value', value)
    def get(self,request):
        if('username' in request.session):
            print(os.listdir())
            df = pd.read_csv("detail.csv")

            df = df.sort_values(by='Date that the company has come')
            df = df.reset_index(drop=True)
            a = list(df['CTC'])
            print(len(a))
            first=float(a[-1].replace(',',''))
            first = first/100000
            second = float(a[-2].replace(',',''))
            second = second/100000
            to_be_predicted=np.array([[second,first]])
            to_be_predicted = to_be_predicted.reshape(to_be_predicted.shape[0],to_be_predicted.shape[1],1)
            all_plots = []
            all_plots += ctc(df)
            plot2 = wordCloud(df)
            global value
            return render(request,self.template_name,{"all_plots":all_plots,"wordCloud": plot2,'next':str(self.value[0][0])})
        else:
            return redirect('/accounts/login')


class SearchCompany(TemplateView):
    api_name = "Search Company api"
    result = CompanyInfo.objects
    summary_objects = []
    category_objects = []
    nlp = spacy.load("en_core_web_md")
    names = []
    summaries = []
    categories = []
    for item in result:
        names.append(item["Name"])
        summaries.append(item["Summary"])
        print(item["Categories"])
        categories.append(",".join(item["Categories"]))
        summary_obj = nlp(item["Summary"])
        tokens = [token.text for token in summary_obj if not token.is_stop]
        summary_objects.append(nlp(" ".join(tokens)))
        category_objects.append(nlp(" ".join(item["Categories"])))

    def get(self, request):
        print(self.api_name)
        search_request = request.GET["search_field"]
        print(search_request)
        search_request_object = self.nlp(search_request)
        similarities = []
        for i in range(len(self.summary_objects)):
            similarities.append([" ".join(self.names[i].split("_")), self.summaries[i],
                                 self.categories[i], self.summary_objects[i].similarity(search_request_object),
                                 self.category_objects[i].similarity(search_request_object)])
        for i in range(len(similarities)):
            similarities[i].append(similarities[i][3] + similarities[i][4])
        similarities.sort(key=lambda x: x[5], reverse=True)
        similarities = similarities[0:5]
        for s in similarities:
            print(s[0])
            print(s[5])
            print("\n")
        request.session["search_query"] = request.GET["search_field"]
        request.session["search_results"] = similarities
        return redirect("/students/searchResults")


class SearchView(TemplateView):
    def get(self, request):
        search_form = SearchForm()
        return render(self.request, 'search.html', {'search_form': search_form})


class SearchResultsView(TemplateView):
    def get(self, request):
        return render(self.request, 'results.html', {"search_query": request.session["search_query"],
                                                     "search_results": request.session["search_results"]})


class SkillRefine(TemplateView):
    template_name = 'quiz/skills_home.html'

    def get(self, request):
        if 'username' in request.session:
            user = User.objects.get(srn=request.session['username'])
            score_op = user['score_op']
            score_al = user['score_al']
            score_ds = user['score_ds']
            score_cn = user['score_cn']

            data = [go.Bar(x=['Algorithms', 'Networking', 'Data Science', 'OOPs'],
                           y=[score_al, score_cn, score_ds, score_op])]
            layout = dict(title='Performance Report', xaxis=dict(title="Subject"),
                          yaxis=dict(title="Score"))
            fig = go.Figure(data=data, layout=layout)
            fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            plots = [fig]
            return render(request, 'quiz/skills_home.html', {"plots": plots})


class QuizPage(TemplateView):
    template_name = 'quiz/quiz_page.html'
    result = None

    def get(self, request):
        QuizPage.result = request.GET['subject']
        return render(request, self.template_name, {'subject': QuizPage.result})

    def post(self, request):
        result = QuizPage.result
        if result == 'op':
            with open('../skill_questions/oops.json') as json_file:
                q_data = json.load(json_file)
        elif result == 'cn':
            with open('../skill_questions/networking.json') as json_file:
                q_data = json.load(json_file)
        elif result == 'ds':
            with open('../skill_questions/datascience.json') as json_file:
                q_data = json.load(json_file)
        elif result == 'al':
            with open('../skill_questions/algos.json') as json_file:
                q_data = json.load(json_file)
        q_data.append({'subject': result})
        print(q_data)
        return JsonResponse(q_data, safe=False)


class QuizPageResults(TemplateView):
    print("ninaad is here")
    def get(self, request):
        print("hi")
        if 'username' in request.session:
            user = User.objects.get(srn=request.session['username'])
            srn = user['srn']
            sub = request.GET['subject']
            numCorrect = request.GET['numCorrect']
            total = request.GET['total']
            if sub == 'al':
                User.objects(srn=srn).update_one(score_al=float((int(numCorrect)/int(total))*100))
            elif sub == 'cn':
                User.objects(srn=srn).update_one(score_cn=float((int(numCorrect)/int(total))*100))
            elif sub == 'ds':
                User.objects(srn=srn).update_one(score_ds=float((int(numCorrect)/int(total))*100))
            elif sub == 'op':
                User.objects(srn=srn).update_one(score_op=float((int(numCorrect)/int(total))*100))
            return HttpResponse("updated")
