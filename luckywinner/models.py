from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Luckydraw(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='luckywinner')
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return(self.name)

class Participants(models.Model):
    facebook_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    link = models.CharField(max_length=1000, null=True)
    luckydraw = models.ForeignKey(Luckydraw, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return(self.name)

class Winner(models.Model):
    luckydraw = models.ForeignKey(Luckydraw, on_delete=models.SET_NULL, related_name='luckydraw_name', null=True)
    name = models.ForeignKey(Participants, on_delete=models.SET_NULL, related_name='participant_name', null=True)

