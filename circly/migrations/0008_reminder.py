# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0007_auto_20150913_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('reminder_subject', models.CharField(max_length=65)),
                ('reminder_message', models.CharField(max_length=150)),
                ('reminder_created_date', models.DateTimeField(verbose_name=b'date of event')),
                ('reminder_send_date', models.DateTimeField(null=True, verbose_name=b'date of event', blank=True)),
                ('reminder_sent', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='circly.Member')),
            ],
        ),
    ]
