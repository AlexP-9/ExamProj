from django.db.models import Count, F

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required

from .forms import FormAddTrip, FormAddImage, FormAddSchedule, FormGuide
from .models import Guide, Schedule, Trip, TripGallery

from datetime import datetime

"""
#Administrational views
"""
@staff_member_required
def view_managing_panel(request):
    return render(request,"Managing/ManagingPanel.html")


#################################################################################
@staff_member_required
def view_trip_list(request):
    dbtrips=Trip.objects.all()
    return render(request, "Managing/TripList.html",{
        "dbtrips":dbtrips
    })

@staff_member_required
def view_trip_add(request):
    formtrip=FormAddTrip()
    if(request.method=="POST"):
        formtrip=FormAddTrip(request.POST)
        #formim=FormAddImages(request.POST, request.FILES)
        #print(formtrip.is_valid())
        #print(formim.is_valid())
        #if((formtrip.is_valid())and(formim.is_valid())):
        if(formtrip.is_valid()):
            #Save the trip itself
            tripinfo=formtrip.save()

            #Alright! Proceed to adding the images
            messages.add_message(request, messages.INFO, "Successfully added a new advenure!")
            return redirect("trip_man_pics", tid=tripinfo.id)
    
    return render(request,"Managing/TripEdit.html",{
        "FormTrip":formtrip,
        #"FormIm":formim,
        "edit":False
    })

@staff_member_required
def view_trip_manage_pics(request, tid):
    currenttrip=get_object_or_404(Trip, id=tid)
    if(request.method=="POST"):
        formpic=FormAddImage(request.POST, request.FILES)
        if(formpic.is_valid()):
            TripGallery(trip=currenttrip, picture=formpic.cleaned_data["picture"]).save()
            messages.add_message(request, messages.INFO, "Successfully saved the picture!")
    picsdb=TripGallery.objects.filter(trip=currenttrip)
    print(picsdb)
    formimg=FormAddImage()
    return render(request, "Managing/TripPics.html",{
        "picsdb":picsdb,
        "formimg":formimg,
        "nextid":tid
    })

@staff_member_required
def view_pic_delete(request, pid):
    picobj=get_object_or_404(TripGallery, id=pid)
    next=request.GET.get("next","")
    if(not next):
        next="view_trip_list"
    return render(request, "Managing/PicDelete.html",{
        "next":next,
        "picobj":picobj
    })

@staff_member_required
def view_pic_delete_confirm(request, pid):
    picobj=get_object_or_404(TripGallery, id=pid)
    picobj.delete()
    messages.add_message(request, messages.INFO, "The picture was successfully deleted!")
    next=request.GET.get("next","")
    if(next):
        return redirect(next)
    return redirect("view_trip_list")


@staff_member_required
def view_trip_edit(request, tid):
    tripdb=get_object_or_404(Trip, id=tid)
    if(request.method=="POST"):
        formtrip=FormAddTrip(request.POST, instance=tripdb)
        if(formtrip.is_valid()):
            #Save the trip itself
            tripinfo=formtrip.save()

            #Alright! Proceed to adding the images
            messages.add_message(request, messages.INFO, "Successfully saved changes!")
            return redirect("trip_man_pics", tid=tripinfo.id)
    else:
        formtrip=FormAddTrip(instance=tripdb)

    return render(request,"Managing/TripEdit.html",{
        "FormTrip":formtrip,
        "edit":True
    })

@staff_member_required
def view_trip_delete(request, tid):
    tripobj=get_object_or_404(Trip, id=tid)
    return render(request, "Managing/TripDelete.html",{
        "t":tripobj
    })

@staff_member_required
def view_trip_delete_confirm(request, tid):
    tripobj=get_object_or_404(Trip, id=tid)
    tripobj.delete()
    messages.add_message(request, messages.INFO, "Trip was successfully deleted!")
    return redirect("manage_trips")  

#################################################################################

@staff_member_required
def view_schedule_list(request):
    scheddb=Schedule.objects.all()
    today=datetime.today().date()
    schedpast=scheddb.filter(end__lt=today).order_by('end')
    schedfuture=scheddb.filter(start__gt=today).order_by('start')
    schedactive=scheddb.filter(start__lte=today, end__gte=today).order_by('start')
    return render(request,"Managing/ScheduleList.html",{
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
                messages.add_message(request, messages.INFO, "Successfully scheduled a new advenure!")
                return redirect("manage_schedule")

            messages.add_message(request, messages.INFO, f"There is an overlap with existing schedule! ({len(overlaps)} conflict{'s' if len(overlaps)>1 else ''}): "+";\n".join(str(o) for o in overlaps))       
    else:
        formsched=FormAddSchedule()
    return render(request,"Managing/ScheduleEdit.html",{
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
    return render(request,"Managing/ScheduleEdit.html",{
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
    return render(request, "Managing/ScheduleDelete.html",{
        "s":schedobj,
    })

@staff_member_required
def view_schedule_delete_conf(request, sched_id):
    schedobj=get_object_or_404(Schedule, id=sched_id)
    schedobj.delete()
    messages.add_message(request, messages.INFO, "The entry was successfully deleted!")
    return redirect("manage_schedule")  

#################################################################################
@staff_member_required
def view_guide_list(request):
    dbguides=Guide.objects.all()
    return render(request, "Managing/GuideList.html",{
        "dbguides":dbguides
    })

@staff_member_required
def view_guide_add(request):
    if(request.method=="POST"):
        formguid=FormGuide(request.POST, request.FILES)
        if(formguid.is_valid()):
            formguid.save()
            messages.add_message(request, messages.INFO, "Successfully added a new guide!")
            return redirect("manage_guides")
    else:
        formguid=FormGuide()
    return render(request,"Managing/GuideEdit.html",{
        "FormGuid":formguid
    })

@staff_member_required
def view_guide_edit(request, gid):
    dbguide=get_object_or_404(Guide, id=gid)
    if(request.method=="POST"):
        formguid=FormGuide(request.POST, instance=dbguide)
        if(formguid.is_valid()):
            formguid.save()
            messages.add_message(request, messages.INFO, "Changes saved successfully!")
            return redirect("manage_guides")   
    else:
        formguid=FormGuide(instance=dbguide)
    return render(request,"Managing/GuideEdit.html",{
        "GuideEdit":True,
        "FormGuid":formguid
    })

@staff_member_required
def view_guide_delete(request, gid):
    guideobj=get_object_or_404(Guide, id=gid)
    return render(request, "Managing/GuideDelete.html",{
        "g":guideobj
    })
    
@staff_member_required
def view_guide_delete_confirm(request, gid):
    guideobj=get_object_or_404(Guide, id=gid)
    guideobj.delete()
    messages.add_message(request, messages.INFO, "The guide was successfully deleted!")
    return redirect("manage_guides")  
#################################################################################