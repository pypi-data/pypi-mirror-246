# Generated by Django 2.2.9 on 2020-01-21 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_add_signing_service_model'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='publishedartifact',
            unique_together={('publication', 'relative_path')},
        ),
    ]
