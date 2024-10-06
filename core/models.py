from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

class Profile(models.Model):
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('legal_aid', 'Legal Aid'),
        ('admin', 'Admin'),
    ]

    # Add a unique related_name to avoid conflicts
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='core_profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image exists before opening it
        if self.image and os.path.exists(self.image.path):
            img = Image.open(self.image.path)

            # Resize the image if it's larger than 300x300
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        else:
            print("Image not found, using default image.")
