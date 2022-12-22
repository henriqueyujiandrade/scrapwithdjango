from django.db import models
import uuid
# Create your models here.
class Monitor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    price = models.TextField()
    category = models.TextField()
    store = models.TextField()
    link = models.URLField()