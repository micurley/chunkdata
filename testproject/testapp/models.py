from django.db import models

class TestPerson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class TestLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(blank=True, max_length=2)
    postal_code = models.CharField(blank=True, max_length=10)