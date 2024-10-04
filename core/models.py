from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.core.files.storage import FileSystemStorage
#from datetime import datetime
from django.utils import timezone

User = get_user_model()


# Create your models here.

class Graphical(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    img1 = models.CharField(max_length=100,blank=False)
    img2 = models.CharField(max_length=100,blank=False)
    img3 = models.CharField(max_length=100,blank=False)

    def __str__(self) :
        return self.user.username
