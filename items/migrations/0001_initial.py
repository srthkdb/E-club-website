# Generated by Django 2.1.3 on 2018-12-09 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=500)),
                ('item', models.CharField(max_length=500)),
                ('quantity_total', models.IntegerField()),
                ('quantity_left', models.IntegerField()),
                ('location', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Issued',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_issued', models.IntegerField()),
                ('issue_or_use', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('return_number', models.CharField(default='', max_length=500)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Box')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]