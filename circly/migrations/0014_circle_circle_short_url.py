# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0013_auto_20151005_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='circle_short_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
