# Generated by Django 3.1.7 on 2021-08-23 22:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0013_auto_20210823_2242'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JobApplicants',
            new_name='JobApplicant',
        ),
    ]