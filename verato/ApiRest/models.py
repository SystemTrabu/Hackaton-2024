from django.db import models

# Create your models here.

class ussers(models.Model):
    _id=models.AutoField(primary_key=True)
    prefix=models.CharField(max_length=5)
    FirstName=models.CharField(max_length=50)
    MiddleName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50)
    suffix=models.CharField(max_length=5)
    Alias_1=models.CharField(max_length=50)
    Alias_2=models.CharField(max_length=50) 
    Alias_3=models.CharField(max_length=50)
    DateOfBirth=models.DateField
    SSN=models.DateField(max_length=9)
    Address1Line1=models.CharField(max_length=50)
    Address1Line2 = models.CharField(max_length=255, blank=True, null=True)
    Address1City = models.CharField(max_length=100)
    Address1State = models.CharField(max_length=50)
    Address1Zip = models.CharField(max_length=10)
    Address1Zip4 = models.CharField(max_length=4, blank=True, null=True)
    Address2Line1 = models.CharField(max_length=255, blank=True, null=True)
    Address2Line2 = models.CharField(max_length=255, blank=True, null=True)
    Address2City = models.CharField(max_length=100, blank=True, null=True)
    Address2State = models.CharField(max_length=50, blank=True, null=True)
    Address2Zip = models.CharField(max_length=10, blank=True, null=True)
    Address2Zip4 = models.CharField(max_length=4, blank=True, null=True)
    Phone1AreaCode = models.CharField(max_length=3)
    Phone1BaseNumber = models.CharField(max_length=7)
    Phone2AreaCode = models.CharField(max_length=3, blank=True, null=True)
    Phone2BaseNumber = models.CharField(max_length=7, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])


