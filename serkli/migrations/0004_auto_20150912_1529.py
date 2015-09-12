# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serkli', '0003_auto_20150912_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='member_phone',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_email',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
