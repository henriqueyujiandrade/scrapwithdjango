from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=127)
    birthdate = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "birthdate"]