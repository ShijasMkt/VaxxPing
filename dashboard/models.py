from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Increase length for hashed passwords

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)  # Hash password before saving
        super().save(*args, **kwargs)

class Patients(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField( blank=True,null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    
class Vaccines(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    code_name=models.CharField(max_length=20,unique=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  
    interval_days = models.PositiveIntegerField(default=0,blank=True,null=True)  
    created_at = models.DateTimeField(auto_now_add=True)


class VaccineSchedule(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="vaccine_schedules")
    vaccine = models.ForeignKey(Vaccines, on_delete=models.CASCADE, related_name="vaccine_schedules")
    scheduled_date = models.DateField()
    notes = models.TextField(blank=True, null=True)  # Optional notes
    created_at = models.DateTimeField(auto_now_add=True)
