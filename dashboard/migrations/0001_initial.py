# Generated by Django 4.1.5 on 2023-04-18 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thresholds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature_min', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('temperature_max', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('voltage_min', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('voltage_max', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]