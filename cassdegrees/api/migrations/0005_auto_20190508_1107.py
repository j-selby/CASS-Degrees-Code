# Generated by Django 2.1.7 on 2019-05-08 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190501_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmodel',
            name='staffNotes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='programmodel',
            name='studentNotes',
            field=models.TextField(blank=True, default=''),
        ),
    ]
