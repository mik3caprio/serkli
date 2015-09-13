# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circly', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('circle_name', models.CharField(max_length=100)),
                ('circle_created_date', models.DateTimeField(verbose_name=b'date of event')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_name', models.CharField(max_length=100)),
                ('member_email', models.CharField(max_length=200)),
                ('sex_range', models.CharField(default=b'XX', max_length=2, choices=[(b'XX', b'XX sex chromosomes (female)'), (b'XY', b'XY sex chromosomes (male)')])),
                ('ethnicity_range', models.CharField(default=b'CNH', max_length=3, choices=[(b'CNH', b'Caucasian Non-Hispanic'), (b'AFR', b'African American'), (b'HIS', b'Hispanic'), (b'ASI', b'Asian'), (b'OTH', b'Other race or ethnicity')])),
                ('age_range', models.CharField(default=b'<25', max_length=3, choices=[(b'<25', b'is less than 25'), (b'25>', b'is 25 or greater')])),
                ('smoker', models.BooleanField(default=False)),
                ('drinker', models.BooleanField(default=False)),
                ('exercises', models.BooleanField(default=False)),
                ('cancer_family', models.SmallIntegerField(default=0)),
                ('circle', models.ForeignKey(to='circly.Circle')),
            ],
        ),
    ]
