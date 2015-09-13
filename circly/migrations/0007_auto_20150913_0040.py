# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0006_auto_20150912_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='age_range',
            field=models.CharField(default=b'20-29', max_length=5, choices=[(b'<20', b'under 20'), (b'20-29', b'between 20 and 29'), (b'30-39', b'between 30 and 39'), (b'40-44', b'between 40 and 44'), (b'45-49', b'between 45 and 49'), (b'50-59', b'between 50 and 59'), (b'>60', b'60 and over')]),
        ),
    ]
