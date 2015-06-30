# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0018_post_nsfw'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reddit_name',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
