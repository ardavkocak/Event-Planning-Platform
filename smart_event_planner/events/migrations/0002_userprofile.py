# Generated by Django 5.0.4 on 2024-11-29 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(default='profile_pics/default_profile.png', upload_to='profile_pics/')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('interests', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
