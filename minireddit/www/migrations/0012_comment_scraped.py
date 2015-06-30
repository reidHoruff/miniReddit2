# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0011_post_scraped'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='scraped',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
