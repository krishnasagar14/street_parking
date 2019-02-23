import uuid
from django.db import models

# Create your models here.

class baseModel(models.Model):
    """
    This is book keeping model for storing created_at, updated_at of record in tables.
    This can be utilized for other app's models.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, \
                          db_index=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now_add=True)
    created_by = models.CharField('Created By', max_length=10, default='app')