# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0002_auto_20150621_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sub',
            field=models.ForeignKey(to='www.Sub', null=True),
        ),
    ]
