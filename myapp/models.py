from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=30, default='')
    
    def __str__(self):
        return self.name