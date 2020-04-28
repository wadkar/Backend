from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from .models import *
from .forms import ContactForm, enquiryform
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context
from django.template.loader import get_template ,render_to_string
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives


from rest_framework.viewsets import ViewSet
from .serializers import *
from rest_framework.response import Response

from process_health import get_score

def home(request):
    return TemplateResponse(request,'home/home.html',{})

def results(request):
    if request.method == 'POST':
        data = request.POST
        #who answering for?

        input_array = {}
        if data['gender']=='Male':
            input_array['gender']=1
        elif data['gender']=='Female':
            input_array['gender']=-1
        else:
            input_array['gender']=0

        input_array['age'] = int(data['age'])

        input_array['height'] = float(data['height'])

        input_array['weight'] = 0

        input_array['hr'] = 0
        input_array['bp'] = 0

        input_array['contact'] = 1 if data['contact']=='Yes' else 0
        input_array['international'] = 1 if data['international']=='Yes' else 0
        input_array['domestic'] = 1 if data['domestic']=='Yes' else 0
        #other illness?
        input_array['immunocompromised'] = 1 if data['immunocompromised']=='Yes' else 0

        input_array['sore_throat'] = 1 if data['throat']=='Yes' else 0
        input_array['fever'] = int(data['fevercheck'])
        input_array['coughcheck'] = 1 if data['coughcheck']=='Yes' else 0
        input_array['shortnesscheck'] = int(data['shortnesscheck'
        ])
        input_array['hypertension'] = 1 if data.get('hypertension','')=='Yes' else 0
        input_array['diabetes'] = 1 if data.get('diabetes','')=='Yes' else 0
        input_array['stroke'] = 1 if data.get('stroke','')=='Yes' else 0
        input_array['lung'] = 1 if data.get('lung','')=='Yes' else 0
        input_array['heart'] = 1 if data.get('heart','')=='Yes' else 0
        input_array['kidney'] = 1 if data.get('kidney','')=='Yes' else 0
        input_array['transplant'] = 0
        input_array['fatigue'] = 1 if data['fatigue']=='Yes' else 0
        input_array['taste'] = 1 if data['taste']=='Yes' else 0
        input_array['headache'] = 1 if data['headache']=='Yes' else 0
        input_array['muscle'] = 1 if data['muscle']=='Yes' else 0
        input_array['chill'] = 1 if data['chill']=='Yes' else 0

        input_array['nausea'] = 1 if data['nausea']=='Yes' else 0
        input_array['nasal'] = 1 if data['nasal']=='Yes' else 0
        input_array['diarrhea'] = 1 if data['diarrhea']=='Yes' else 0
        input_array['time'] = int(data['time'
        ])
        input_array['symp'] = int(data['symp'
        ])
        input_array['alert'] = 1 if data['alert']=='Yes' else 0

        health_score = get_score(input_array)

        context={'health_score':health_score}

        return render(request,'home/response.html',context=context)
