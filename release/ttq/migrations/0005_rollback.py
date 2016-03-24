# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ttq', '0004_projects_back_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rollback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(blank=True, max_length=200, null=True)),
                ('backtofile', models.CharField(blank=True, max_length=200, null=True)),
                ('rollback_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('results', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(to_field='username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
