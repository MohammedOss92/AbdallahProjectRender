from django.db import models

# Create your models here.


# ##################################

class MeesageType(models.Model):
    MsgTypes = models.CharField(max_length=100, null=True)
    new_msg = models.CharField(max_length=2,default=1)
    new_msgs_text = models.CharField(max_length=2, null=True, default=1)
    created_at_new_msgs_text = models.DateField(null=True)
    updated_at_new_msgs_text = models.DateField(null=True)
    my_time_auto = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.MsgTypes

class Messages(models.Model):
    #CharField was CharField has become 
    MessageName = models.TextField( null=True)
    ID_Type = models.ForeignKey(MeesageType, null=True, on_delete=models.SET_NULL)
    new_msgs = models.CharField(max_length=2, null=False, default=1)
    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    new_msgs_text = models.CharField(max_length=2, null=False, default=1)
    created_at_new_msgs_text = models.DateField(null=True)
    updated_at_new_msgs_text = models.DateField(null=True)
    my_time_auto = models.TimeField(auto_now_add=True)
    day_num = models.CharField(max_length=2, null=False, default=0)
    
    def __str__(self):
        return self.MessageName



