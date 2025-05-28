from django.db.models import Count, F

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import FormAddTrip, FormAddImages, FormAddSchedule
from .models import Guide, Review, Schedule, Trip, TripGallery

from datetime import datetime

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
            return redirect("main_page")
            #return redirect(request.GET.get("next",""))
        messages.add_message(request, messages.WARNING, "Incorrect password!")
        return render(request,"LogIn.html",{
            "username":uname            
        })
    return render(request, "LogIn.html")

def view_logout(request):
    logout(request)
    return redirect("main_page")

def view_register(request):
    
    return render(request, "Register.html")

def view_profile(request):
    return render(request,"Profile.html")

"""
#Trip views (all, individual, etc.)
"""
def view_mainpage(request):
    tripsdb=Trip.objects.all
    #availsched=Schedule.objects.filter(start__gt=datetime.today().date(), maxattendants__gt=Count("attendants"))
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    return render(request, "MainPage.html",
                  {
                      "trips":tripsdb,
                      "availsched":availsched
                  })

def view_trip(request, tid):
    tripdb=get_object_or_404(Trip,id=tid)
    picsdb=TripGallery.objects.filter(trip__id=tid)
    reviewsdb=Review.objects.filter(revtrip=tid)
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(trip__id=tid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    return render(request, "TripPage.html",
                  {
                      "tripobj":tripdb,
                      "picobjs":picsdb,
                      "reviews":reviewsdb,
                      "schedule":availsched
                  })

def view_trip_full_schedule(request, tid):
    tripdb=get_object_or_404(Trip,id=tid)
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(trip__id=tid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    return render(request, "TripFullSchedule.html",{
        "tripobj":tripdb,
        "schedule":availsched
    })

def view_all_trips(request):
    all_trips = Trip.objects.all()
    return render(request, "AllTrips.html", {
        "trips": all_trips
    })

def view_trip_register(request, sid):   #SID = Schedule ID, so that we could filter out the old and fully-booked trips
    #scheddb=Schedule.objects.filter(id=sid) #This is a workaround so that the user doesn't get a 404 error
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(id=sid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')

    return render(request, "TripRegister.html",{
        "scheddb":availsched
    })

@login_required
def view_trip_register_confirm(request, sid):
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(id=sid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    if(not availsched):
        #Nope!
        return render(request, "TripRegister.html",
                      {"scheddb":None})
    if(availsched[0].attendants.contains(request.user.customer)):
        #Nope!
        messages.add_message(request, messages.INFO, "Your are already registered for this trip!")
        return redirect("main_page")
    availsched[0].attendants.add(request.user.customer)
    availsched[0].save()
    messages.add_message(request, messages.SUCCESS, "Successfully registered for the trip!")
    return redirect("main_page")

"""
#Administrational views
"""
@staff_member_required
def view_managing_panel(request):
    return render(request,"ManagingPanel.html")

@staff_member_required
def view_add_trip(request):
    formtrip=FormAddTrip()
    formim=FormAddImages()
    if(request.method=="POST"):
        formtrip=FormAddTrip()
        formim=FormAddImages()
        uplimages=request.FILES.getlist("picture")
        print("Post")
        print(request.FILES)
        for i in uplimages:
            print(i)
    
    return render(request,"AdminAddTrip.html",{
        "FormTrip":formtrip,
        "FormIm":formim
    })

@staff_member_required
def view_schedule(request):
    scheddb=Schedule.objects.all()
    today=datetime.today().date()
    schedpast=scheddb.filter(end__lt=today)
    schedfuture=scheddb.filter(start__gt=today)
    schedactive=scheddb.filter(start__lte=today, end__gte=today)
    return render(request,"Schedule.html",{
        "SchedObjsPast":schedpast,
        "SchedObjsFuture":schedfuture,
        "SchedObjsActive":schedactive,
    })

@staff_member_required
def view_schedule_add(request):
    if(request.method=="POST"):
        formsched=FormAddSchedule(request.POST)
        if(formsched.is_valid()):
            #Check if we have overlaps
            #If there are different guides assigned, then, of course,
            #the schedules may overlap
            cleandata=formsched.cleaned_data
            overlaps=set(Schedule.objects.filter(
                    start__lte=cleandata["end"],
                    end__gte=cleandata["start"],
                    guides__in=cleandata["guides"]
                ))
            if(len(overlaps)==0):
                formsched.save()
                messages.add_message(request, messages.INFO, "Successfully added a new advenure!")
                return redirect("manage_schedule")

            messages.add_message(request, messages.INFO, f"There is an overlap with existing schedule! ({len(overlaps)} conflicts): "+";\n".join(str(o) for o in overlaps))       
    else:
        formsched=FormAddSchedule()
    return render(request,"ScheduleAdd.html",{
        "FormSched":formsched
    })

@staff_member_required
def view_schedule_edit(request, sched_id):
    sched=get_object_or_404(Schedule, id=sched_id)
    if(request.method=="POST"):
        formsched=FormAddSchedule(request.POST, instance=sched)
        if(formsched.is_valid()):
            #Check if we have overlaps
            #If there are different guides assigned, then, of course,
            #the schedules may overlap
            cleandata=formsched.cleaned_data
            overlaps=set(Schedule.objects.filter(
                    start__lte=cleandata["end"],
                    end__gte=cleandata["start"],
                    guides__in=cleandata["guides"]
                ).exclude(id=sched_id))
            if(len(overlaps)==0):
                formsched.save()
                messages.add_message(request, messages.INFO, "Changes saved successfully!")
                return redirect("manage_schedule")   
            messages.add_message(request, messages.INFO, f"There is an overlap with existing schedule! ({len(overlaps)} conflicts): "+";\n".join(str(o) for o in overlaps))
    else:
        formsched=FormAddSchedule(instance=sched)
    return render(request,"ScheduleAdd.html",{
        "ScheduleEdit":True,
        "FormSched":formsched
    })

@staff_member_required
def view_schedule_delete(request, sched_id):
    schedobj=get_object_or_404(Schedule, id=sched_id)
    """
    if(request.method=="DELETE"):
        messages.add_message(request, messages.INFO, "The entry was successfully deleted!")
        return redirect("manage_schedule")  
    """
    return render(request, "ScheduleDelete.html",{
        "s":schedobj,
    })

@staff_member_required
def view_schedule_delete_conf(request, sched_id):
    schedobj=get_object_or_404(Schedule, id=sched_id)
    schedobj.delete()
    messages.add_message(request, messages.INFO, "The entry was successfully deleted!")
    return redirect("manage_schedule")  

"""
#Debug
"""
def view_debug(request):
    return render(request,"Debug.html")


"""
#Misc. stuff
"""

def view_about(request):
    guidesdb=Guide.objects.all
    return render(request, "About.html",
                  {
                      "guides":guidesdb
                  })

def view_contact(request):
    return render(request, "Contact.html")