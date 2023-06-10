from django.db import models
from django.contrib.auth.models import User
from users.models import *



class Bookmodel(models.Model):

    p_user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    bookname = models.CharField(max_length=255, blank=False, null=True)
    bookid = models.CharField(max_length=255, blank=False, null=True)
    bookstatus = models.CharField(max_length=255, blank=False, null=True)
    bookrating = models.CharField(max_length=255, blank=False, null=True)
    bookgenre = models.CharField(max_length=255, blank=False, null=True)
    bookoverallrating = models.CharField(max_length=255, blank=False, null=True)
    bookvote = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self) -> str:
        return  f"{self.p_user}"
