# Generated by Django 3.2.3 on 2021-05-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_appointment_appointment_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='app_date',
            field=models.DateField(),
        ),
    ]