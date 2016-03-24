# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ttq', '0003_auto_20160316_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='back_path',
            field=models.CharField(default='/data/backup/www/', max_length=100),
        ),
    ]
