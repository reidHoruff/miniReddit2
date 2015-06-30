# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0019_post_reddit_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumb',
            field=models.CharField(default=None, max_length=1000, null=True),
            preserve_default=True,
        ),
    ]
