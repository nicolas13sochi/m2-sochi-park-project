from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def uuid_as_string(self):
        return str(self.uuid)

    class Meta:
        abstract = True
