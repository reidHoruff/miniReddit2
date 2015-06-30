# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0012_comment_scraped'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_cache',
            field=models.TextField(default=b'{}'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='comments_cache_invalid',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
