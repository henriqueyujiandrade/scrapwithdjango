from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Monitor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    current_price = models.TextField()
    category = models.TextField()
    store = models.TextField()
    link = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
