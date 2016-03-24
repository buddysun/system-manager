# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='script',
            field=models.CharField(max_length=100, default='/data/yunwei/shell/njw_update.sh'),
        ),
        migrations.AlterField(
            model_name='release',
            name='filename',
            field=models.FileField(upload_to='/buddy/release/uploads'),
        ),
    ]
