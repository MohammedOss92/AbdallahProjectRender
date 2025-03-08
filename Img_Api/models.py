from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
import os

# Create your models here.

class ImageType(models.Model):
    ImgTypes = models.CharField(max_length=100, null=True)
    new_img = models.CharField(max_length=2,default=1)

    def __str__(self):
        return self.ImgTypes



class Imgs(models.Model):
     ID_Type = models.ForeignKey(ImageType, null=True, on_delete=models.SET_NULL)
     pic = models.ImageField(upload_to='')
     new_img = models.CharField(max_length=2, null=True,default=1)
     image_url = models.URLField(null=True, blank=True)
     created_at = models.DateField(auto_now_add=True)
     updated_at = models.DateField(auto_now=True)
     new_msgs_text = models.CharField(max_length=2, null=True, default=1)
     created_at_new_msgs_text = models.DateField(null=True)
     updated_at_new_msgs_text = models.DateField(null=True)
     my_time_auto = models.TimeField(auto_now_add=True)

