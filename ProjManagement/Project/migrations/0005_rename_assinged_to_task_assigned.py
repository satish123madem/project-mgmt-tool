# Generated by Django 5.0.3 on 2024-03-25 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0004_rename_creataed_by_task_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='assinged_to',
            new_name='assigned',
        ),
    ]
