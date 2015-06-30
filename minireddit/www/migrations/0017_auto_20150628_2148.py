# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0016_auto_20150628_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='datetime',
            field=models.DateTimeField(default=datetime.date(2015, 6, 28), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='datetime',
            field=models.DateTimeField(default=datetime.date(2015, 6, 28), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sub',
            name='datetime',
            field=models.DateTimeField(default=datetime.date(2015, 6, 28), auto_now=True),
            preserve_default=False,
        ),
    ]
