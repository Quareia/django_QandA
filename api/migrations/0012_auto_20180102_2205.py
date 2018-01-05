# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 14:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_userinfo_userimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='ansimage',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='userimg',
            field=models.ImageField(blank=True, default='', upload_to='images'),
        ),
    ]
