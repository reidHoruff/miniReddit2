# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('www', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(related_name=b'created_subs', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(related_name=b'subscribed_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='sub',
            field=models.ForeignKey(default=None, to='www.Sub'),
            preserve_default=False,
        ),
    ]
