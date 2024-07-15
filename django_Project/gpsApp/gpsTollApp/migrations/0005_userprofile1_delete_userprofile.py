# Generated by Django 5.0.7 on 2024-07-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpsTollApp', '0004_alter_userprofile_super_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=50, unique=True)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(default='', max_length=10)),
                ('address', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=50)),
                ('password', models.CharField(default='', max_length=50)),
                ('super_user', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
