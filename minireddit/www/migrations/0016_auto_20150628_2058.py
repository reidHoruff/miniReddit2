# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0015_post_reddit_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='domain',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='is_self',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
