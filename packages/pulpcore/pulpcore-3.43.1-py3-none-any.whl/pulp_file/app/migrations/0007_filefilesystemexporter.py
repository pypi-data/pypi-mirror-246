# Generated by Django 2.2.6 on 2020-03-17 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_change_exporter_models'),
        ('file', '0006_delete_filefilesystemexporter'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileFileSystemExporter',
            fields=[
                ('exporter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='file_filefilesystemexporter', serialize=False, to='core.Exporter')),
                ('path', models.TextField()),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
            },
            bases=('core.exporter',),
        ),
    ]
