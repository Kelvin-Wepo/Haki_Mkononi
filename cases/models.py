from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):
    CATEGORY_CHOICES = [
        ('civil', 'Civil'),
        ('criminal', 'Criminal'),
        ('family', 'Family'),
        ('commercial', 'Commercial'),
        ('labor', 'Labor'),
    ]
    
    STATUS_CHOICES = [
        ('under_review', 'Under Review'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='under_review')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_cases')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)  
    location_county = models.CharField(max_length=100, null=True, blank=True)
    location_Area = models.CharField(max_length=100, null=True, blank=True)
    date_of_occurrence = models.DateField(null=True, blank=True)
    parties_involved = models.JSONField(null=True, blank=True)  # Using JSONField to store flexible data
    court_jurisdiction = models.CharField(max_length=200, null=True, blank=True)
    evidence = models.TextField(null=True, blank=True)  # Store evidence details (e.g., witnesses, physical evidence)

    def __str__(self):
        return self.title

class Document(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='case_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
