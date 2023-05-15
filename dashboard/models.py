from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Thresholds(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=1, default=('0.00'))
    temperature_max = models.DecimalField(max_digits=5, decimal_places=1, default=('30.00'))
    power_min = models.DecimalField(max_digits=5, decimal_places=1, default=('0.00'))
    power_max = models.DecimalField(max_digits=5, decimal_places=1, default=('20.00'))


class LayoutData(models.Model):
    ID = models.IntegerField(primary_key=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    voltage = models.DecimalField(max_digits=5, decimal_places=1)
    current = models.DecimalField(max_digits=5, decimal_places=1)
    power = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'layout_data'
        managed = False