from django.db import models
from django.utils import timezone

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']


class Project(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('in Progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True)


    project_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=255) 
    type = models.CharField(max_length=50) 
    division = models.CharField(max_length=50)  
    category = models.CharField(max_length=50)  
    priority = models.CharField(max_length=50)  
    department = models.CharField(max_length=50)  
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
