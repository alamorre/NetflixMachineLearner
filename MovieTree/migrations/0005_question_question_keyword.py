# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-19 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieTree', '0004_auto_20161119_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_keyword',
            field=models.CharField(default='null', max_length=200),
        ),
    ]