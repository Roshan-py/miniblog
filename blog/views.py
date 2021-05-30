from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm, ContactForm
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from    django.contrib.auth.models import Group
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.


# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})


# About
def about(request):
    return render(request, 'blog/about.html')


# contactus
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Inquiry'
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name' : form.cleaned_data['last_name'],
                'email' : form.cleaned_data['email_address'],
                'message' : form.cleaned_data['message'],
            }
            message = '\n'.join(body.values())

            try:
                send_mail(subject,message,'admin@example.com',['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            return HttpResponseRedirect('/')
    else:
        form=ContactForm()
    return render(request, 'blog/contactus.html',{'form':form})


# Dashboard

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        group = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts,'full_name':full_name,'groups':group })
    else:
        return HttpResponseRedirect('/login/')

# signup
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! you have successfully signed up...')
            user=form.save()
            group= Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html', {'form': form})

# Signout

def user_signout(request):
    logout(request)
    return HttpResponseRedirect('/')


# login
def user_signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form= LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname =form.cleaned_data['username']
                upass =form.cleaned_data['password']
                user= authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'logged in Successfully !!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

#add new post

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form= PostForm(request.POST)
            if form.is_valid():
                form.save()
        else:
                form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#Update post

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Post Updated..!')
        else:
            pi = Post.objects.get(pk=id)
            form= PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#Delete post

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')



