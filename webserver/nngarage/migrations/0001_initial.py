# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 22:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=30)),
                ('content', models.FileField(upload_to=b'files')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('learning_rate', models.FloatField()),
                ('num_iter', models.IntegerField()),
                ('out_dim', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(auto_now_add=True)),
                ('completed_status', models.CharField(default=b'Incompleted', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='model', to='nngarage.FileBase')),
                ('parameter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parameter', to='nngarage.FileBase')),
                ('test_in', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test_in', to='nngarage.FileBase')),
                ('test_out', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='test_out', to='nngarage.FileBase')),
                ('train_in', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='train_in', to='nngarage.FileBase')),
                ('train_out', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='train_out', to='nngarage.FileBase')),
            ],
        ),
    ]
