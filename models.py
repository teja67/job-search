from django.db import models
from datetime import date

# Create your models here.

class Skill(models.Model):
    user_id = models.CharField(max_length=255, default='default_user')
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    job = models.CharField(max_length=150, default='')
    job_desc = models.CharField(max_length=255, default='')
    date_posted = models.DateField(default=date.today)
    salary = models.CharField(max_length=255, default='')
    vacancy = models.IntegerField(default=0)
    contact = models.CharField(max_length=255)

class City(models.Model):
    city_name=models.CharField(max_length=255)

    def __str__(self):
            return self.city_name
    

class Location(models.Model):
    city_id=models.ForeignKey(City,on_delete=models.CASCADE)
    location_name=models.CharField(max_length=255)    
    
    def __str__(self):
        return self.location_name
    
class Job_applications(models.Model):
    user_id=models.IntegerField(default='')    
    job_id=models.IntegerField(default='')    
    name=models.CharField(max_length=255,default='')    
    email=models.CharField(max_length=255,default='')    
    description=models.CharField(max_length=255,default='')    
    contact=models.CharField(max_length=255,default='')    