from django.db.models import Count, F, Q, Avg

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ReviewForm, FormRegister, FormChangeData, FormChangePassword
from .models import Guide, Review, Schedule, Trip, TripGallery, Customer, User, Tag, Difficulty

from datetime import datetime

# Create your views here.

"""
#Registration, Login, Logout
"""
def view_login(request):
    if(not request.user.is_authenticated):
        if(request.method=="POST"):
            uname=request.POST.get("username")
            passw=request.POST.get("password")
            user=authenticate(request,username=uname,password=passw)
            if user:    #if user is not None:
                login(request,user)
                next=request.GET.get("next","")
                if(next):
                    return redirect(next)
                return redirect("main_page")
            messages.add_message(request, messages.WARNING, "Incorrect password!")
            return render(request,"Accounts/LogIn.html",{
                "username":uname            
            })
        return render(request, "Accounts/LogIn.html")
    else:
        next=request.GET.get("next","")
        if(next):
            return redirect(next)
        return redirect("main_page")   

def view_logout(request):
    logout(request)
    next=request.GET.get("next","")
    if(next):
        return redirect(next)
    return redirect("main_page")

def view_register(request):
    if(not request.user.is_authenticated):
        regform=FormRegister()
        if(request.method=="POST"):
            regform=FormRegister(request.POST)
            if(regform.is_valid()):
                regform.save()
                authuser=authenticate(request,username=regform.cleaned_data["username"],password=regform.cleaned_data["password1"])
                login(request,authuser)
                customer=Customer(user=authuser,
                                phone=regform.cleaned_data["phone"],
                                newsletter=regform.cleaned_data["newsletter"])
                customer.save()
                next=request.GET.get("next","")
                if(next):
                    return redirect(next)
                return redirect("main_page")
        return render(request, "Accounts/Register.html",{
            "regform":regform
        })
    else:
        next=request.GET.get("next","")
        if(next):
            return redirect(next)
        return redirect("main_page")   

@login_required
def view_profile(request):
    schedactive=Schedule.objects.filter(start__lte=datetime.now(),end__gte=datetime.now(),attendants__id=request.user.id).order_by('end')
    schedfuture=Schedule.objects.filter(start__gte=datetime.now(),attendants__id=request.user.id).order_by('start')
    schedpast=Schedule.objects.filter(end__lte=datetime.now(),attendants__id=request.user.id).order_by('start')

    profile=get_object_or_404(User, id=request.user.id)
    custdb=Customer.objects.filter(user=request.user)
    
    return render(request,"Accounts/Profile.html",{
        "schedactive":schedactive,
        "schedfuture":schedfuture,
        "schedpast":schedpast,
        "profile":profile,
        "customer":custdb
    })

@login_required
def view_trip_history(request):
    schedactive=Schedule.objects.filter(start__lte=datetime.now(),end__gte=datetime.now(),attendants__id=request.user.id).order_by('end')
    schedfuture=Schedule.objects.filter(start__gte=datetime.now(),attendants__id=request.user.id).order_by('start')
    schedpast=Schedule.objects.filter(end__lte=datetime.now(),attendants__id=request.user.id).order_by('start')
    return render(request,"Accounts/ProfileTripHistory.html",{
        "schedactive":schedactive,
        "schedfuture":schedfuture,
        "schedpast":schedpast
    })

@login_required
def view_account_edit_data(request):
    if(request.user.is_staff):
        return redirect("profile")
    dbuser=User.objects.get(id=request.user.id)
    dbcustomer=Customer.objects.get(user=request.user)

    if(request.method=="POST"):
        forminfo=FormChangeData(request.POST, instance=dbuser)
        if(forminfo.is_valid()):
            dbuser.username=forminfo.cleaned_data["username"]
            dbuser.first_name=forminfo.cleaned_data["first_name"]
            dbuser.last_name=forminfo.cleaned_data["last_name"]
            dbcustomer.phone=forminfo.cleaned_data["phone"]
            dbcustomer.newsletter=forminfo.cleaned_data["newsletter"]
            dbuser.save()
            dbcustomer.save()
            messages.add_message(request, messages.INFO, "Data changed successfully!")
            return redirect("profile")
    else:
        forminfo=FormChangeData()
        forminfo.initial["username"]=dbuser.username
        forminfo.initial["first_name"]=dbuser.first_name
        forminfo.initial["last_name"]=dbuser.last_name
        forminfo.initial["phone"]=dbcustomer.phone
        forminfo.initial["newsletter"]=dbcustomer.newsletter

    
    return render(request, "Accounts/ChangeInfo.html",{
        "forminfo":forminfo
    })

@login_required
def view_account_new_password(request):
    if(request.method=="POST"):
        formpass=FormChangePassword(request.POST)
        print(formpass.fields)
        if(request.user.check_password(request.POST['oldpassword'])):
            if(formpass.is_valid()):
                changeduser=User.objects.get(id=request.user.id)
                changeduser.set_password(formpass.cleaned_data["password1"])
                changeduser.save()
                messages.add_message(request, messages.INFO, "Password changed successfully!")
                return redirect("profile")
        else:
            formpass.add_error("oldpassword","Incorrect old password!")
    else:
        formpass=FormChangePassword()

    return render(request, "Accounts/ChangePassword.html",{
        "formpass":formpass
    })

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
    tripdb=get_object_or_404(Trip,id=tid)   #Yeah, it's intended :-)
    tripdb=Trip.objects.annotate(avgrating=Avg("review__rating")).get(id=tid)
    picsdb=TripGallery.objects.filter(trip__id=tid)
    reviewsdb=Review.objects.filter(revtrip=tid)

    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(trip__id=tid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    
    if(request.user.is_authenticated):
        registered=Schedule.objects.filter(trip__id=tid, end__gt=datetime.now(),attendants__id=request.user.id)
        availsched=availsched.filter(~Q(id__in=registered))
    else:
        registered=None

    visited=User.objects.filter(schedules__trip=tid, schedules__end__lte=datetime.now(),id=request.user.id).exists()
    
    user_review=reviewsdb.filter(customer__id=request.user.id).first()
    reviewsshown=reviewsdb.filter(~Q(customer__id=request.user.id))
    
    commentform=ReviewForm(instance=user_review)
    if(user_review):
        editing_review=True
    else:
        editing_review=False
    
    if(request.method=="POST"):
        commentform=ReviewForm(request.POST, instance=user_review)
        if(commentform.is_valid()):
            if(user_review):
                #OK, edit this review
                user_review.revtitle=commentform.cleaned_data["revtitle"]
                user_review.comment=commentform.cleaned_data["comment"]
                user_review.rating=commentform.cleaned_data["rating"]
                user_review.save()
            else:
                #This is a new review
                Review(revtitle=commentform.cleaned_data["revtitle"],
                        comment=commentform.cleaned_data["comment"],
                        rating=commentform.cleaned_data["rating"],
                        customer=request.user,
                        revtrip=tripdb
                        ).save()
        return redirect("trip",tid=tid)
            
   
    return render(request, "Trips/TripPage.html",
                  {
                      "tripobj":tripdb,
                      "picobjs":picsdb,
                      "reviews":reviewsshown,
                      "reviews_count":reviewsdb.count(),
                      "schedule":availsched,
                      "visited":visited,
                      "registered":registered,
                      "commentform":commentform,
                      "editing_review":editing_review
                  })

def view_trip_full_schedule(request, tid):
    tripdb=get_object_or_404(Trip,id=tid)
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(trip__id=tid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    return render(request, "Trips/TripFullSchedule.html",{
        "tripobj":tripdb,
        "schedule":availsched
    })

def view_all_trips(request):
    #all_trips = Trip.objects.all()
    all_tags=Tag.objects.all()
    all_difficulties=Difficulty.objects.all()

    reqget=request.GET
    if(reqget):
        all_filt_tags=[key for key in reqget.items() if key[0].startswith("Tag_")]
        if(len(all_filt_tags)!=0):
            filt_tags=[t[0][4:] for t in all_filt_tags if(t[1]=="on")]
        else:
            filt_tags=[t.name for t in all_tags]

        all_filt_diffs=[key for key in reqget.items() if key[0].startswith("Diff_")]
        if(len(all_filt_diffs)!=0):
            filt_diffs=[d[0][5:] for d in all_filt_diffs if(d[1]=="on")]
        else:
            filt_diffs=[d.name for d in all_difficulties]
        
        wordsearch=reqget.get("wordsearch","")
        returned_trips=Trip.objects.all().filter(Q(title__icontains=wordsearch) | Q(description__icontains=wordsearch), tags__name__in=filt_tags, difficulty__name__in=filt_diffs)
    else:
        returned_trips = Trip.objects.all()
    
    returned_trips=returned_trips.annotate(avgrating=Avg("review__rating"))
    
    return render(request, "Trips/AllTrips.html", {
        "trips": returned_trips,#all_trips,
        "tags": all_tags,
        "difficulties":all_difficulties
    })

def view_trip_register(request, sid):   #SID = Schedule ID, so that we could filter out the old and fully-booked trips
    #scheddb=Schedule.objects.filter(id=sid) #This is a workaround so that the user doesn't get a 404 error
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(id=sid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start').first()
    
    if(request.user.is_authenticated):
        overlaps=set(Schedule.objects.filter(
                        start__lte=availsched.end,
                        end__gte=availsched.start,
                        attendants__id=request.user.id
                    ))
        if(availsched.attendants.contains(request.user)):
            #Nope!
            messages.add_message(request, messages.INFO, "Your are already registered for this trip!")
            return redirect("main_page")
    else:
        overlaps=set([])

    return render(request, "Trips/TripRegister.html",{
        "scheddb":availsched,
        "overlaps":overlaps
    })

@login_required
def view_trip_register_confirm(request, sid):
    availsched=Schedule.objects.annotate(att_count=Count("attendants")).filter(id=sid, start__gt=datetime.today().date(), att_count__lt=F("maxattendants")).order_by('start')
    if(not availsched):
        #Nope!
        return render(request, "Trips/TripRegister.html",
                      {"scheddb":None})
    
    print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",333)
    if(availsched[0].attendants.contains(request.user)):
        #Nope!
        messages.add_message(request, messages.INFO, "You are already registered for this trip!")
        return redirect("main_page")
    availsched[0].attendants.add(request.user)
    availsched[0].save()
    messages.add_message(request, messages.SUCCESS, "Successfully registered for the trip!")
    return redirect("main_page")



"""
#Debug
"""
def view_debug(request):
    r=request.GET.get("next","")
    print("++++")
    print(r)
    if(r):
        print("ifr")
    print("++++")
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
