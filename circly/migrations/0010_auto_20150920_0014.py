# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0009_auto_20150919_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='reminder_sent',
        ),
        migrations.AddField(
            model_name='circle',
            name='circle_reminders_refreshed_on_date',
            field=models.DateTimeField(null=True, verbose_name=b'reminders refreshed on', blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='circle_owner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='member_profile_entered_date',
            field=models.DateTimeField(null=True, verbose_name=b'profile entered on', blank=True),
        ),
        migrations.AddField(
            model_name='reminder',
            name='member_reminded_on_date',
            field=models.DateTimeField(null=True, verbose_name=b'member reminded on', blank=True),
        ),
        migrations.AddField(
            model_name='reminder',
            name='reminder_sent_on_date',
            field=models.DateTimeField(null=True, verbose_name=b'reminder sent on', blank=True),
        ),
    ]
