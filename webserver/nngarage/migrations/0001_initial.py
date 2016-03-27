# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NetDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('file_ins', models.FileField(upload_to=b'net_description/file/%m/%d/%Y')),
                ('screenshot', models.ImageField(upload_to=b'net_description/image/%m/%d/%Y')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password1', models.CharField(default=b'', max_length=100, blank=True)),
                ('password2', models.CharField(default=b'', max_length=100, blank=True)),
                ('first_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('image', models.ImageField(upload_to=b'profile-photos/%m/%d/%Y')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
