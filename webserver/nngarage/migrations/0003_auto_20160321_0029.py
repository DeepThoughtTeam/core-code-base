# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nngarage', '0002_auto_20160320_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='finish_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='model',
            field=models.OneToOneField(related_name='model', null=True, to='nngarage.FileBase'),
        ),
    ]
