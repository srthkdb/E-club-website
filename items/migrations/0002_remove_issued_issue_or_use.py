# Generated by Django 2.1.3 on 2018-12-09 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issued',
            name='issue_or_use',
        ),
    ]
