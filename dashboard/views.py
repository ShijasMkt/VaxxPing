from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import check_password
from dashboard.models import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from datetime import date
from .models import VaccineSchedule
from .utils import send_whatsapp_message

# Create your views here.
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    if 'user_id' in request.session:
        return redirect('dashboard')
    

    if request.method=='POST':
        uname=request.POST.get('uName')
        password=request.POST.get('pass')

        user=Users.objects.filter(username=uname).first()

        if user:
            if check_password(password,user.password):
                user_id=user.id
                request.session['user_id']=user_id

                return redirect('dashboard')
            else:
                messages.error(request,"Incorrect Password!!")
                return redirect('login')
        else:
            messages.error(request,"Invalid User!!") 
            return redirect('login')   
              
    
    return render(request,'login.html')

def logoutView(request):
    request.session.flush()
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboardView(request):
    if 'user_id' in request.session:
        user_id=request.session['user_id']
        user = Users.objects.get(id=user_id)  
        return render(request, 'dashboard.html', {'user': user})
    else:
        return redirect('login')
    
    

def add_patient(request):
    if 'user_id' not in request.session:
        return redirect('login')

    
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        contact_number = request.POST.get('contact_number', '')
        email = request.POST['email']
        address = request.POST['address']

        patient = Patients(
            name=name,
            age=age,
            gender=gender,
            contact_number=contact_number,
            email=email,
            address=address
        )
        patient.save()
        messages.success(request,"Patient added successfully!!")
        return redirect('add_patient')  
    return render(request, 'add_patients.html')

def add_vaccine(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST['name']
        code_no = request.POST['code_no']
        manufacturer = request.POST.get('manufacturer', '')
        description = request.POST.get('description', '')
        interval_days = request.POST.get('interval_days')  


        
        if Vaccines.objects.filter(name=name).exists():
            messages.error(request, "Vaccine with this name already exists!")
            return redirect('add_vaccine')

        
        vaccine = Vaccines(
            name=name,
            code_name=code_no,
            manufacturer=manufacturer,
            description=description,
            interval_days=interval_days
        )
        vaccine.save()

        messages.success(request, "Vaccine added successfully!")
        return redirect('add_vaccine')
    

    return render(request, 'add_vaccine.html')
    
def schedule_vaccine(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    patient_data = Patients.objects.all()
    vaccine_data = Vaccines.objects.all()
    
    if request.method == 'POST':
        patient_id = request.POST.get("patient")
        vaccine_id = request.POST.get("vaccine")
        appointment_date = request.POST.get("appointment_date")
        notes = request.POST.get("notes", "")
        
        if not patient_id or not vaccine_id or not appointment_date:
            messages.error(request, "All fields are required.")
            return redirect("schedule_vaccine")
        
        # Get patient and vaccine objects
        patient = Patients.objects.filter(id=patient_id).first()
        vaccine = Vaccines.objects.filter(id=vaccine_id).first()

        if not patient or not vaccine:
            messages.error(request, "Invalid patient or vaccine selection.")
            return redirect('schedule_vaccine')

        
        # Create appointment entry
        VaccineSchedule.objects.create(
            patient=patient,
            vaccine=vaccine,
            scheduled_date=appointment_date,
            notes=notes
        )
        
        messages.success(request, "Vaccine appointment scheduled successfully!")
        return redirect("schedule_vaccine")
    
    return render(request, 'schedule_vaccine.html', {"patients": patient_data, "vaccines": vaccine_data})
    
def view_schedules(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    schedules=VaccineSchedule.objects.select_related('patient',"vaccine").all()



    return render(request,'view_schedules.html',{'schedules':schedules})



def send_vaccine_reminders(request):  # Accept 'request' parameter
    today = date.today()
    schedules = VaccineSchedule.objects.filter(scheduled_date=today)

    sent_messages = []  # Store sent messages for response

    for schedule in schedules:
        patient = schedule.patient
        if patient.contact_number:
            message = f"Hello {patient.name}, your vaccine '{schedule.vaccine.name}' is scheduled for today. Please visit your clinic."
            response = send_whatsapp_message(patient.contact_number, message)
            sent_messages.append({"patient": patient.name, "message": response})

    return JsonResponse({"status": "success", "sent_messages": sent_messages})
