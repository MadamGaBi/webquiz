# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer',
            new_name='answer_text',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='question_text',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_2',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_3',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_4',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_5',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_desc',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_description',
            field=models.CharField(default=datetime.datetime(2015, 7, 17, 14, 6, 18, 463889, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
