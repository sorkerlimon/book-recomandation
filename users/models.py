from django.db import models
from django.contrib.auth.models import User


     

class user_profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    dob = models.DateField(max_length=8,blank=True,null=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self) -> str:
        return self.name
