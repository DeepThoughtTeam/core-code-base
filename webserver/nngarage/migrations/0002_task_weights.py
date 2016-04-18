# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nngarage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='weights',
            field=models.OneToOneField(related_name='weights', null=True, to='nngarage.FileBase'),
        ),
    ]
