# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 16:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilerGuiFile',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('filer.file',),
        ),
    ]
