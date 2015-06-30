# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_auto_20150623_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent_id',
            new_name='parent',
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name=b'comments', to='www.Post'),
        ),
    ]
