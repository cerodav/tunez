# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Tunez_home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='size',
            field=models.CharField(max_length=20, default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userquery',
            name='query_date',
            field=models.DateTimeField(verbose_name='date created', default=datetime.datetime(2015, 5, 29, 0, 24, 56, 711938)),
        ),
    ]
