from django.db import models
from django.contrib.auth.models import User

class VideoCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_calls')
    official = models.ForeignKey(User, on_delete=models.CASCADE, related_name='official_calls')
    room_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')

    def __str__(self):
        return f"Call between {self.user.username} and {self.official.username}"