# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0011_auto_20150924_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invites',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('invite_created_date', models.DateTimeField(verbose_name=b'invite created on')),
                ('invite_send_date', models.DateTimeField(null=True, verbose_name=b'send invite on', blank=True)),
                ('invite_sent_on_date', models.DateTimeField(null=True, verbose_name=b'invite sent on', blank=True)),
                ('member_joined_on_date', models.DateTimeField(null=True, verbose_name=b'member joined on', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='ethnicity_range',
            field=models.CharField(default=b'CNH', max_length=3, choices=[(b'CNH', b'Caucasian'), (b'AFR', b'African American'), (b'HIS', b'Hispanic'), (b'ASI', b'Asian'), (b'OTH', b'Other')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='sex_range',
            field=models.CharField(default=b'XX', max_length=2, choices=[(b'XX', b'female (XX)'), (b'XY', b'male (XY)')]),
        ),
        migrations.AddField(
            model_name='invites',
            name='member',
            field=models.ForeignKey(to='circly.Member'),
        ),
    ]
