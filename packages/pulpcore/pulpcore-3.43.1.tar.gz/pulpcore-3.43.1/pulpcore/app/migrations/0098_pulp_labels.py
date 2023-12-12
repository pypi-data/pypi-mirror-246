# Generated by Django 3.2.16 on 2022-11-28 08:30

import django.contrib.postgres.fields.hstore
from django.db import migrations

from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_remove_telemetry_task_schedule'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='distribution',
            name='pulp_labels',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
        migrations.AddField(
            model_name='remote',
            name='pulp_labels',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
        migrations.AddField(
            model_name='repository',
            name='pulp_labels',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
    ]
