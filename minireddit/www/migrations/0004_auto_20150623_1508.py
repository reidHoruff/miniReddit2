# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('www', '0003_auto_20150621_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent_id', models.ForeignKey(to='www.Comment')),
                ('post', models.ForeignKey(to='www.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='post',
            name='sub',
            field=models.ForeignKey(to='www.Sub'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.CharField(max_length=1000),
        ),
    ]
