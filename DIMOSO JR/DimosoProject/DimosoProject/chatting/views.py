from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import calendar
from calendar import HTMLCalendar
from DimosoApp.models import *
from DimosoApp.forms import *
from hitcount.views import HitCountDetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
import json

# Create your views here.
def chatroom(request, pk:int):
    other_user = get_object_or_404(MyUser, pk=pk)
    messages = Message.objects.filter(
        Q(receiver=other_user, sender=request.user) | Q(receiver=request.user, sender=other_user)
    )
    messages.update(seen=True)
    context = {
	"other_user": other_user,
	#'users': MyUser.objects.all(),
	"messages": messages
      }
    #messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user) )
    return render(request, "chatting/chatroom.html", context)


    

def ajax_load_messages(request, pk):
    other_user = get_object_or_404(MyUser, pk=pk)
    #messages = Message.objects.filter(seen=False)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=other_user, sender=request.user) | Q(receiver=request.user, sender=other_user)
     
    )
    messages.update(seen=True)
    
    #print("messages")
    message_list = [{
        "sender": message.sender.username,
        "message": message.message,
        "sent": message.sender == request.user
       # "picture": other_user.profile.picture.url,

        #"date_created": naturaltime(message.date_created),

    } for message in messages]
    #messages.update(seen=True)
    
    if request.method == "POST":
        message = json.loads(request.body)
        
        m = Message.objects.create(receiver=other_user, sender=request.user, message=message)
        message_list.append({
            "sender": request.user.username,
            #"username": request.user.username,
            "message": m.message,
            #"date_created": naturaltime(m.date_created),

           # "picture": request.user.profile.picture.url,
            "sent": True,
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)