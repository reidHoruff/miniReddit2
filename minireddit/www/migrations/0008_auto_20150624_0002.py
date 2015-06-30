# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('www', '0007_auto_20150623_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(related_name=b'votes', to='www.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(related_name=b'votes', to='www.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(related_name=b'children', to='www.Comment', null=True),
        ),
    ]
