from django.db import models
import uuid

class Account(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255)  # Name field added
    Balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Name
