# Generated by Django 3.1.7 on 2021-08-23 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20210820_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(null=True),
        ),
    ]