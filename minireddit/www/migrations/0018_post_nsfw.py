# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0017_auto_20150628_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nsfw',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
