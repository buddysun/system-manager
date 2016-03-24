# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hostname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.IntegerField(default=22)),
                ('commd', models.CharField(max_length=200)),
                ('results', models.TextField(blank=True, null=True)),
                ('exec_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ipaddr', models.ManyToManyField(to='ttq.Hostlist', db_constraint='ip')),
                ('user', models.ForeignKey(to_field='username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=38, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('port', models.IntegerField(default=22)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(blank=True, max_length=200, null=True)),
                ('filename', models.FileField(upload_to='/data/django/release/uploads')),
                ('release_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('results', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(to_field='username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Uploads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destIPs', models.CharField(blank=True, max_length=200, null=True)),
                ('filename', models.FileField(upload_to='/buddy/release/uploads')),
                ('upload_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('remoteDir', models.CharField(blank=True, max_length=100, null=True)),
                ('remotefile', models.CharField(blank=True, max_length=100, null=True)),
                ('remoteIP', models.ManyToManyField(to='ttq.Hostlist')),
                ('user', models.ForeignKey(to_field='username', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
