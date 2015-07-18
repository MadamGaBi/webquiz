# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('correct_answer', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('correct_answer', models.CharField(max_length=100)),
                ('answer_2', models.CharField(max_length=100)),
                ('answer_3', models.CharField(max_length=100)),
                ('answer_4', models.CharField(max_length=100)),
                ('answer_5', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Results',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'Students',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
                ('topic_desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'Tutors',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='student_id',
            field=models.ForeignKey(to='exam.Student'),
        ),
        migrations.AddField(
            model_name='result',
            name='topic_id',
            field=models.ForeignKey(to='exam.Topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='topic_id',
            field=models.ForeignKey(to='exam.Topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='tutor_id',
            field=models.ForeignKey(to='exam.Tutor'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(to='exam.Question'),
        ),
    ]
