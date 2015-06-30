# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0014_auto_20150628_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reddit_id',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
