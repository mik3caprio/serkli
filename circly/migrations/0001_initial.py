# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendee_id', models.CharField(max_length=50)),
                ('attendee_email', models.CharField(max_length=200)),
                ('attendee_name', models.CharField(max_length=100)),
                ('checked_in', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=200)),
                ('event_date', models.DateTimeField(verbose_name=b'date of event')),
            ],
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(to='circly.Event'),
        ),
    ]
