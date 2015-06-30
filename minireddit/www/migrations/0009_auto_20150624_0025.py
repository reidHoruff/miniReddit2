# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0008_auto_20150624_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(related_name=b'comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name=b'posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
