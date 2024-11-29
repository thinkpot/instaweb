from django.db import models
from .validators import validate_phone_number


class ServicesProvided(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Leads(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    service_interest = models.ForeignKey(ServicesProvided, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.email