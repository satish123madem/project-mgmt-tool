# Generated by Django 5.0.3 on 2024-03-25 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0003_rename_cretaed_by_task_creataed_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='creataed_by',
            new_name='created_by',
        ),
    ]
