from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import FormAddTrip, FormAddImages

# Create your views here.
"""
#Registration, Login, Logout
"""
def view_login(request):
    if(request.method=="POST"):
        uname=request.POST.get("username")
        passw=request.POST.get("password")
        user=authenticate(request,username=uname,password=passw)
        if user:    #if user is not None:
            login(request,user)
            return redirect(request.GET.get("next",""))
        messages.add_message(request, messages.WARNING, "Incorrect password!")
        return render(request,"LogIn.html",{
            "username":uname            
        })
    return render(request, "LogIn.html")

def view_logout(request):
    logout(request)
    return redirect("")

def view_register(request):
    return render()

"""
#Trip views (all, individual, etc.)
"""
def view_mainpage(request):
    return render(request, "MainPage.html")

def view_trip(request, tid):
    return render(request, "TripPage.html")

"""
#Administrational views
"""
#@staff_member_required
def view_admin_panel(request):
    return render(request,"AdminPanel.html")

#@staff_member_required
def view_add_trip(request):
    formtrip=FormAddTrip()
    formim=FormAddImages()
    if(request.method=="POST"):
        return render(request,"AdminAddTrip.html")
    return render(request,"AdminAddTrip.html",{
        "FormTrip":formtrip,
        "FormIm":formim
    })
