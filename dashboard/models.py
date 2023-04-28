from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Thresholds(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    voltage_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    voltage_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    predicted_voltage_min = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    predicted_voltage_max = models.DecimalField(max_digits=5, decimal_places=1, null=True)

    def __str__(self):
        return f'Thresholds for {self.user.username}'


class LayoutData(models.Model):
    ID = models.IntegerField(primary_key=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    humidity = models.DecimalField(max_digits=5, decimal_places=1)
    voltage = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        db_table = 'layout_data'
        managed = False