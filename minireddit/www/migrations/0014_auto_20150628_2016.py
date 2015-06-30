# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0013_auto_20150628_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments_cache',
        ),
        migrations.RemoveField(
            model_name='post',
            name='comments_cache_invalid',
        ),
    ]
