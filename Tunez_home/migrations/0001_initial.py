# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=20)),
                ('quality', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=400)),
                ('downloaded', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='userquery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('query_content', models.CharField(max_length=200)),
                ('query_date', models.DateTimeField(default=datetime.datetime(2015, 5, 28, 19, 19, 2, 528895), verbose_name='date created')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='query',
            field=models.ForeignKey(to='Tunez_home.userquery'),
        ),
    ]
