# Generated by Django 5.0.4 on 2024-12-01 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
