# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0010_post_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='scraped',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
