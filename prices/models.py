from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Price(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    price = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    monitor = models.ForeignKey(
        "monitors.Monitor", on_delete=models.CASCADE, related_name="prices", null=True
    )
