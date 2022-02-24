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
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
	
def base(request):
    social = SocialMedia.objects.all()
    context={
        "social":social,
    }
    return render(request, 'DimosoApp/base.html',context)

def uchafu(request):
    social = SocialMedia.objects.all()
    context={
        "social":social,
    }
    return render(request, 'DimosoApp/uchafu.html', context)




def home(request, category_slug=None):
    form = PostForm(request.POST or None)

    
    
    
    posti = Post.objects.all().order_by('id')
    new_posts = Post.objects.all().order_by('-id')[:6]
    category = None
    categories = Category.objects.all()
    form = PostForm(request.POST or None)# form ya kuserch ila nimeifuta nimetumia hzo code za chini

    
    #searching button codes
    if request.method == 'POST':
        posti = Post.objects.filter( name__icontains=form['name'].value())
#hizi codes ni kwa ajili ya kudisplay category 
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        posti= posti.filter(category=category)
#zinaishia hapa
    context = {
        "form":form,
        "categories":categories, 
        "category":category,
        "new_posts":new_posts,

        "posti":posti
    }

    return render(request, 'DimosoApp/home.html', context)

def search_post(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(name__icontains=query_original) 
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    posti = Post.objects.filter(search)
    mylist= []
    mylist += [x.name for x in posti]
    return JsonResponse(mylist, safe=False)


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'DimosoApp/postdetail.html'
    count_hit = True

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            messages.success(request, "message sent successfully")

            return redirect(reverse("PostDetail", kwargs={
                    'pk':post.pk

                }))
    def get_context_data(self, **kwargs):
        new_posts = Post.objects.all().order_by('-id')[:6]
        #to count number of comment
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
#kwa ajili ya kudisplay comment huo mstari wa chini
        post_comments = Comment.objects.all().filter(post=self.object.id)
#zinaendelea za kupost comment kwa admin
        context = super().get_context_data(**kwargs)
        #context["form"] = self.form
        context.update({
                'form':self.form,
                'post_comments':post_comments,
                'post_comments_count':post_comments_count,
                'new_posts':new_posts,
            })
        return context

def post_comments(request):
    post_comments = Comment.objects.all().order_by('-id')

    context = {
        "post_comments":post_comments
    }

    return render(request, 'DimosoApp/post_comments.html', context)    

def blog_users(request):
    blog_users = MyUser.objects.all().order_by('-id')

    context = {
        "blog_users":blog_users
    }

    return render(request, 'DimosoApp/blog_users.html', context)    

class update_blog_user(SuccessMessageMixin, UpdateView):
    model = MyUser
    template_name = 'account/user_register.html'
    form_class = MyUserForm
    success_url = reverse_lazy('blog_users')
    success_message = "User Updated Successfully"  

def delete_blog_user(request, pk):
    user = get_object_or_404(MyUser, id=pk)
    user.delete()
    return redirect('blog_users')

def send_email_to_dimoso(request):
    #Send email function
    if request.method == 'POST':
        
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)
        messages.success(request,"Email sent successfully to juniordimoso8@gmail.com.")
                         
        return redirect('home')

    #INAISHIA HAPA

