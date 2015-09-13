# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0002_circle_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='bmi_range',
            field=models.CharField(default=b'<25', max_length=3, choices=[(b'<25', b'is less than 25'), (b'25>', b'is 25 or greater')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='age_range',
            field=models.CharField(default=b'20-30', max_length=5, choices=[(b'<20', b'under 20'), (b'20-30', b'between 20 and 30'), (b'31-44', b'between 31 and 45'), (b'45-55', b'between 46 and 55'), (b'>55', b'55 and over')]),
        ),
    ]
