# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0008_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_created_date',
            field=models.DateTimeField(null=True, verbose_name=b'member created on', blank=True),
        ),
        migrations.AlterField(
            model_name='circle',
            name='circle_created_date',
            field=models.DateTimeField(verbose_name=b'circle created on'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='reminder_created_date',
            field=models.DateTimeField(verbose_name=b'reminder created on'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='reminder_send_date',
            field=models.DateTimeField(null=True, verbose_name=b'send reminder on', blank=True),
        ),
    ]
