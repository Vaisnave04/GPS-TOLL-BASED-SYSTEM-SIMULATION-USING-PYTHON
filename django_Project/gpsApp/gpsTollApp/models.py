# myapp/models.py
from django.db import models

class userprofile(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, default='')
    address=models.CharField(max_length=200, default='')
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50, default='')
    super_user=models.BooleanField(default=False)

class gpstollapptrip(models.Model):
    trip_id = models.IntegerField(unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    no_tollscrossed = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status=models.CharField(max_length=50)
    trip_date=models.DateField(max_length=25)
    vehicle_regno=models.CharField(max_length=50)
    Applicant_name=models.CharField(max_length=100)
    vehicle_catid=models.IntegerField()
    validity_from=models.DateField(max_length=25)
    validity_to=models.DateField(max_length=25)
    costof_pass = models.DecimalField(max_digits=22, decimal_places=2)
    Vehicle_name=models.CharField(max_length=100)
    distance=models.DecimalField(max_digits=22, decimal_places=2)

class vehiclecategory(models.Model):
    category_id = models.IntegerField(unique=True)
    vehicle_type = models.CharField(max_length=100)
    toll_amount = models.DecimalField(max_digits=22, decimal_places=2)



def __str__(self):
    return self.first_name
    

