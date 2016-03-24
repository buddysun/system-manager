# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttq', '0002_auto_20160222_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200, null=True, blank=True)),
                ('backfile', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='rollback_shell',
            field=models.CharField(max_length=100, default='/data/yunwei/shell/njw_rollback.sh'),
        ),
    ]
