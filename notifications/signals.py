from django.db.models.signals import post_save
from django.dispatch import receiver
from cases.models import Case
from notifications.models import Notification  # Assuming your Notification model is in a separate notifications app

# Signal for case creation
@receiver(post_save, sender=Case)
def case_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.created_by,
            message=f"Your case '{instance.title}' has been successfully created.",
        )

# Signal for case status update (checking 'status' field instead of 'is_resolved')
@receiver(post_save, sender=Case)
def case_status_updated_notification(sender, instance, **kwargs):
    # Notify the user when the case status changes
    if instance.status == 'closed':
        Notification.objects.create(
            user=instance.created_by,
            message=f"Your case '{instance.title}' has been closed.",
        )
    elif instance.status == 'open':
        Notification.objects.create(
            user=instance.created_by,
            message=f"Your case '{instance.title}' has been opened.",
        )
