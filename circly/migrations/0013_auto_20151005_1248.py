# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0012_auto_20151005_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('invite_code', models.CharField(max_length=300, null=True, blank=True)),
                ('invite_short_url', models.URLField(null=True, blank=True)),
                ('invite_created_date', models.DateTimeField(verbose_name=b'invite created on')),
                ('invite_send_date', models.DateTimeField(null=True, verbose_name=b'send invite on', blank=True)),
                ('invite_sent_on_date', models.DateTimeField(null=True, verbose_name=b'invite sent on', blank=True)),
                ('member_joined_on_date', models.DateTimeField(null=True, verbose_name=b'member joined on', blank=True)),
                ('member', models.ForeignKey(to='circly.Member')),
            ],
        ),
        migrations.RemoveField(
            model_name='invites',
            name='member',
        ),
        migrations.DeleteModel(
            name='Invites',
        ),
    ]
