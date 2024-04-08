from django.db import models

class Project(models.Model):
    STATUS_CHOICES = (
        ('Registered', 'Registered'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Registered')
