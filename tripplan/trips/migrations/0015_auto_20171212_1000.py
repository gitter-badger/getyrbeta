# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-12 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0014_auto_20171117_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='itemowner',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
