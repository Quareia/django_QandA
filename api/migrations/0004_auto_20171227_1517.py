# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 07:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20171227_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='followers',
            field=models.ManyToManyField(to='api.UserInfo'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='followers',
            field=models.ManyToManyField(to='api.UserInfo'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='followquestions',
            field=models.ManyToManyField(to='api.Question'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='followtopics',
            field=models.ManyToManyField(to='api.Topic'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL),
        ),
    ]
