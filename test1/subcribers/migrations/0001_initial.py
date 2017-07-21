# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 09:33
from __future__ import unicode_literals

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
            name='Subscrpber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_number', models.CharField(max_length=100)),
                ('event1', models.CharField(max_length=20)),
                ('event2', models.CharField(max_length=20)),
                ('event3', models.CharField(max_length=20)),
                ('email_check', models.IntegerField()),
                ('user_rec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'subscribers',
            },
        ),
    ]
