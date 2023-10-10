from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from testapp.forms import LoginForm,SignUpForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from .models import *


# Create your views here.
def home_view(request):
    return render(request,'testapp/home.html')


from django.contrib.auth import authenticate,login,logout
def custom_login_view(request):
    form=LoginForm()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            # Authentication failed, handle the error
            # return HttpResponse('Authentication failed')
            error_message = "Invalid username or password. Please try again."
            return render(request, 'testapp/custom_login.html', {'form':form,'error_message': error_message})
    return render(request,'testapp/custom_login.html',{'form':form})

def logout_view(request):
    logout(request)
    return render(request,'testapp/logout.html')

def signup_view(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            # user.save()
            login(request, user)
            return HttpResponseRedirect('/custom_login')
    form=SignUpForm()
    return render(request,'testapp/signup.html',{'form':form})


@login_required(login_url='/custom_login/')
def java_page_view(request):
    return render(request,'testapp/javaexams.html')

@login_required(login_url='/custom_login/')
def python_page_view(request):
    return render(request,'testapp/pythonexams.html')

@login_required(login_url='/custom_login/')
def aptitude_page_view(request):
    return render(request,'testapp/aptitudeexams.html')


def forget_password(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request,'Not User found with this username.')
                return redirect('/signup/')

            user_obj=User.objects.get(username=username)

    except Exception as e:
        print(e)