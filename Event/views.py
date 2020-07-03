from django.shortcuts import render ,render_to_response,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages


from django.core.files.storage import FileSystemStorage
from .forms import EmailForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from django.template.loader import get_template
from .utils import render_to_pdf

from matplotlib import pyplot as mp
from matplotlib.backends.backend_agg import FigureCanvasAgg as fig
from matplotlib.figure import Figure
import csv
from io import BytesIO
import array
from django.db.models import Avg,Min,Max,Sum,Count,aggregates,Aggregate



from django.db import connection
# Create your views here.

from random import randint

import requests
import json
URL = 'https://www.way2sms.com/api/v1/sendCampaign'


userno='9657091758'


def LoginView(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            un = request.POST.get('Mobile_No')
            if un==userno:
                return redirect(OTPView)
            else:
                return HttpResponse('invalid no!!')
    else:
        form = LoginForm()
        
    return render(request,'login.html',{'form': form})

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
    req_params = {
    'apikey':apiKey,
    'secret':secretKey,
    'usetype':useType,
    'phone': phoneNo,
    'message':textMessage,
    'senderid':senderId
    }
    return requests.post(reqUrl, req_params)

otp2 = randint(1000,9999)
print(otp2)
api_key='94HBW6MFV1JXBIFU44RVOALZYOM7U41S'
secret_key='258GSOPYZSQE3N3C'
sendto='9657091758'
sendernumber='9028248334'
message=otp2

def OTPView(request):

    #response = sendPostRequest(URL, api_key, secret_key, 'stage', sendto, sendernumber, message )

    if request.method=="POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp1 = int(request.POST.get('Enter_OTP'))
            print(otp1)
            if otp1==otp2:
                return redirect(options)
            else:
                print(otp1)
                return HttpResponse('invalid otp!!')
            
    else:
        form = OTPForm()
    return render(request,'otp.html',{'form':form})
       
def options(request):
    return render_to_response('options.html')

def analyze_optionsView(request):
    return render_to_response('analyze_options.html')


def EventFormView(request):
    if request.method=='POST':
        form=EventForm(request.POST)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()
    else:
        form = EventForm()
        
    return render(request,'form.html',{'form': form})


def SearchView(request): 
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()
            n = request.POST.get('EventName')
            d = request.POST.get('EventDate')
            searched_data = EventModel.objects.raw('SELECT * FROM event_eventmodel WHERE EventName=%s AND EventDate=%s',[n,d])[0]
            id1 = searched_data.id
            return redirect('search_event',id1)
    else:
        form = SearchForm()

    return render(request,'Search.html',{'form': form})



def search_event(request,id=None):
    item=get_object_or_404(EventModel,id=id)
    form=EventForm(request.POST or None,instance=item)
    return render(request,'Searched_content.html',{'form': form})



def EditView(request): 
    if request.method=='POST':
        form=EditForm(request.POST)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()
            n = request.POST.get('EventName')
            d = request.POST.get('EventDate')
            searched_data = EventModel.objects.raw('SELECT * FROM event_eventmodel WHERE EventName=%s AND EventDate=%s',[n,d])[0]
            
            id1 = searched_data.id
            return redirect('edit_event',id1)
    else:
        form = EditForm()
    return render(request,'Edit.html',{'form': form})


def edit_event(request,id=None):
    item=get_object_or_404(EventModel,id=id)
    form=EventForm(request.POST or None,instance=item)
    if form.is_valid():
        name1 = request.POST.get('EventName')
        date1 = request.POST.get('EventDate')
        budg = request.POST.get('Budget')
        desc = request.POST.get('Description')
        no = request.POST.get('NoOfParticipants')
        outc = request.POST.get('Outcomes')
         
        with connection.cursor() as cursor:
            cursor.execute('UPDATE event_eventmodel SET EventName=%s,EventDate=%s,Budget=%s,Description=%s,NoOfParticipants=%s,Outcomes=%s WHERE id=%s',[name1,date1,budg,desc,no,outc,id])
        return render_to_response('a3.html')
    else:
        return render(request,'form.html',{'form': form})



def email(request):
    if request.method == "POST":
        form = EmailForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            document = request.FILES.get('document')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            email = EmailMessage(subject,message,email_from,recipient_list)
            base_dir = 'media/documents/'
            email.attach_file('media/documents/'+str(document))
            email.send()
            return render_to_response('a2.html')
    else:
        form = EmailForm()
            
    return render(request, 'sendemail.html', {'form': form})




def GeneratePDF(request, *args, **kwargs):
    if request.method=="POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()
            
            name1 = request.POST.get('EventName')
            subname1 = request.POST.get('SubEventName')
            date1 = request.POST.get('EventDate')
            budg = request.POST.get('Budget')
            desc = request.POST.get('Description')
            no = request.POST.get('NoOfParticipants')
            outc = request.POST.get('Outcomes')
            #imgs = request.POST.get('images')

            template = get_template('doc.html')
            context = {
                    "EventName": name1,
                    "SubEventName": subname1,
                    "EventDate": date1,
                    "Budget": budg,
                    "Description": desc,
                    "NoOfParticipants": no,
                    "Outcomes": outc,
                    #"images" : imgs
                }
            html = template.render(context)
            pdf = render_to_pdf('doc.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Event_%s.pdf" % (name1)
                content = "inline; filename=%s" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % (filename)
                response['Content-Disposition'] = content #allows user to save file
                return response
            return render_to_response('a1.html')
    
    else:
        form = EventForm()
        return render(request,'form.html',{'form':form})

"""
def display_event_images(request): 
  
    if request.method == 'GET': 
  
        imgs = EventForm.objects.all()  
        return render((request, 'doc.html', 
                     {'event_images' : imgs}))
"""
def EventAnalysisView(request):
    if request.method=='POST':
        form = EventAnalyzeSearchForm(request.POST)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()

            n = request.POST.get('EventName')
            budget_list = []
            part_list = []
            year_list = []
            date_list=[]

        
            result = EventModel.objects.raw("SELECT *,SUM(NoOfParticipants) As part,SUM(Budget) As budget FROM event_eventmodel WHERE EventName=%s GROUP BY EventDate",[n])
            for r in result:
                budget_list.append(r.budget)
                part_list.append(r.part)
                date_list.append(r.EventDate)
            
            for x in date_list:
                year_list.append(str(x.year))
                
            fig = mp.figure()
            fig.patch.set_facecolor("gray")
            graph1 = fig.add_subplot(1, 3, 1)
            graph1.plot(year_list, budget_list, color="orange", label="Line Graph")
            graph1.scatter(year_list, budget_list, color="blue", label="Scatter")
            graph1.bar(year_list, budget_list, color="blue", label="Bar")
            #graph1.legend()
            graph1.set_ylabel("Budget", color="green")
            graph1.set_xlabel("Year", color="green")
            graph1.set_title("Budget for different years", color="red")
            graph1.autoscale(enable=True, axis='both', tight=False)
            graph1.grid(True)

            graph2 = fig.add_subplot(1, 3, 3)
            graph2.plot(year_list, part_list, color="orange", label="Line Graph")
            graph2.scatter(year_list, part_list, color="blue", label="Scatter")
            #graph2.legend()
            graph2.set_ylabel("No of participants", color="green")
            graph2.set_xlabel("Year", color="green")
            graph2.set_title("No of participants ", color="red")
            graph2.autoscale(enable=True, axis='both', tight=False)
            graph2.grid(True)
            buf = BytesIO()
            mp.savefig(buf, format='png')
            mp.close(fig)
            response = HttpResponse(buf.getvalue(), content_type='image/png')
            return response

    else:
        form = EventAnalyzeSearchForm()

    return render(request,'event_analyze.html',{'form': form})


def SubEventAnalysisView(request):
    if request.method=='POST':
        form=AnalyzeSearchForm(request.POST)
        if form.is_valid():
            event_data=form.save(commit=False)
            event_data.save()
            
            n = request.POST.get('EventName')
            s = request.POST.get('SubEventName')
            budget_list = []
            part_list = []
            year_list = []
            date_list=[]    
        
            for abc in EventModel.objects.raw("select * from event_eventmodel where EventName=%s AND SubEventNAme=%s group by EventDate",[n,s]):
           
                budget_list.append(abc.Budget)
                part_list.append(abc.NoOfParticipants)
                date_list.append(abc.EventDate)
          
            for x in date_list:
                year_list.append(str(x.year))
                
            
                
            fig = mp.figure()
            fig.patch.set_facecolor("gray")
            graph1 = fig.add_subplot(1, 3, 1)
            graph1.plot(year_list, budget_list, color="orange", label="Line Graph")
            graph1.scatter(year_list, budget_list, color="blue", label="Scatter")
            graph1.bar(year_list, budget_list, color="blue", label="Bar")
            #graph1.legend()
            graph1.set_ylabel("Budget", color="green")
            graph1.set_xlabel("Year", color="green")
            graph1.set_title("Budget for different years", color="red")
            graph1.autoscale(enable=True, axis='both', tight=False)
            graph1.grid(True)

            graph2 = fig.add_subplot(1, 3, 3)
            graph2.plot(year_list, part_list, color="orange", label="Line Graph")
            graph2.scatter(year_list, part_list, color="blue", label="Scatter")
            #graph2.legend()
            graph2.set_ylabel("No of participants", color="green")
            graph2.set_xlabel("Year", color="green")
            graph2.set_title("No of participants ", color="red")
            graph2.autoscale(enable=True, axis='both', tight=False)
            graph2.grid(True)
            buf = BytesIO()
            mp.savefig(buf, format='png')
            mp.close(fig)
            response = HttpResponse(buf.getvalue(), content_type='image/png')
            return response
        
    else:
        form = AnalyzeSearchForm()

    return render(request,'analyze.html',{'form': form})





import socket

def DetailsView(request):
    if request.method != "POST":
            abc = EventModel.objects.raw('SELECT * FROM event_eventmodel')
            
            str1=""
            for x in abc:
                str1 += str(x.id)+" " +x.EventName+" "+" " +x.SubEventName+" "+ str(x.EventDate)+" "+str(x.Budget)+" "+x.Description+" "+str(x.NoOfParticipants)+" "+str(x.Outcomes)+'\n'
            
            s = socket.socket()
            port = 12345
            s.bind(('', port))
            print("socket binded to %s" % (port))
            s.listen(5)
            print("socket is listening")
            c, addr = s.accept()
            print('Got connection from', addr)
            c.send(bytes(str1,'utf-8'))
            c.close()
            s.close()
            return render_to_response('a.html')
    else:
        return render_to_response('options.html')
