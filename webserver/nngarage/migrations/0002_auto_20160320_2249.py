# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nngarage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=30)),
                ('content', models.FileField(upload_to=b'files')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(default=b'')),
                ('completed_status', models.CharField(default=b'Incompleted', max_length=30)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.OneToOneField(related_name='model', to='nngarage.FileBase')),
                ('parameter', models.OneToOneField(related_name='parameter', to='nngarage.FileBase')),
                ('test_in', models.OneToOneField(related_name='test_in', to='nngarage.FileBase')),
                ('test_out', models.OneToOneField(related_name='test_out', to='nngarage.FileBase')),
                ('train_in', models.OneToOneField(related_name='train_in', to='nngarage.FileBase')),
                ('train_out', models.OneToOneField(related_name='train_out', to='nngarage.FileBase')),
            ],
        ),
        migrations.RemoveField(
            model_name='netdescription',
            name='author',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='NetDescription',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
