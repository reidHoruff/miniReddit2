# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0009_auto_20150624_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
