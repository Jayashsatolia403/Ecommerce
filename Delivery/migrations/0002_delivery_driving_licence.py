# Generated by Django 3.1.7 on 2021-04-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='driving_licence',
            field=models.ImageField(null=True, upload_to='DrivingLicenceDelivery/'),
        ),
    ]
