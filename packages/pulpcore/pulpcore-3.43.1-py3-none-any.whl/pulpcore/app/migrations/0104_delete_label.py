# Generated by Django 3.2.18 on 2023-05-04 07:06

from django.db import migrations
from django.db.models.expressions import OuterRef, RawSQL


def migrate_remaining_labels(apps, schema_editor):
    """
    This data migration handles the "but what about plugins" problem noted in the issue [0], with only two caveats:

    Case 1: If there were to exist a plugin containing a Model whose model-name ended in (for example) "Repository",
    that was NOT a detail-model of a Repository master-model, AND that plugin allowed Labels for such a model - then,
    upon running this migration, those Labels would be lost.

    Case 2: If there were to exist a plugin containing a Model that was a Detail of (for example) Repository,
    but named something like "PluginRepositoryButWhy", and that plugin allowed Labels,
    and instances of such a Model had Labels associated with them - then this migration would fail,
    because the Labels would not be found, migrated, and deleted, and the old-Label table would not be able to be dropped.

    And the plugins described above would have to have existed and been in use with pulpcore/3.21,only -
    if they appeared with core/3.22, they'd be using new-Labels and all would be (already) well.

    No such plugins/Models exist, to the best of our knowledge.

    [0] https://github.com/pulp/pulpcore/issues/4319
    """
    Label = apps.get_model("core", "Label")
    Repository = apps.get_model("core", "Repository")
    Remote = apps.get_model("core", "Remote")
    Distribution = apps.get_model("core", "Distribution")
    ContentType = apps.get_model("contenttypes", "ContentType")

    for master_model, model_name in [(Repository, "repository"), (Remote, "remote"), (Distribution, "distribution")]:
        detail_ctypes = ContentType.objects.filter(app_label__ne="core", model__endswith=model_name)
        affected_ids = Label.objects.filter(content_type__in=detail_ctypes).values("object_id").distinct()
        label_subq = Label.objects.filter(
            content_type__in=detail_ctypes, object_id=OuterRef("pulp_id")
        ).annotate(
            label_data=RawSQL("hstore(array_agg(key), array_agg(value))", [])
        ).values("label_data")
        master_model.objects.filter(pulp_id__in=affected_ids).update(pulp_labels=label_subq)
        Label.objects.filter(content_type__in=detail_ctypes).delete()


def check_no_existing_labels(apps, schema_editor):
    Label = apps.get_model("core", "Label")
    if Label.objects.exists():
        raise RuntimeError(
            "There are remaining labels. Please revert to pulpcore<3.25 and make sure all labels are properly mirgated or deleted."
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0103_alter_export_task'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_remaining_labels,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.RunPython(
            code=check_no_existing_labels,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.RunSQL(
            sql="SET CONSTRAINTS ALL IMMEDIATE;",
            reverse_sql="",
        ),
        migrations.DeleteModel(
            name='Label',
        ),
    ]
