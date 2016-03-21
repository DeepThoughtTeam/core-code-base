# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nngarage', '0003_auto_20160321_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='test_out',
            field=models.OneToOneField(related_name='test_out', null=True, to='nngarage.FileBase'),
        ),
        migrations.AlterField(
            model_name='task',
            name='train_out',
            field=models.OneToOneField(related_name='train_out', null=True, to='nngarage.FileBase'),
        ),
    ]
