# Generated by Django 5.0.7 on 2024-07-14 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpsTollApp', '0002_gpstollapptrip_vehiclecategory_userprofile_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dateofbirth',
        ),
    ]
