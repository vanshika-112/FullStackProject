from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_count = models.IntegerField(null=True, blank=True)
    averages = models.JSONField(null=True, blank=True)
    equipment_distribution = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"