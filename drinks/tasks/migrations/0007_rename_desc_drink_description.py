# Generated by Django 4.2.5 on 2023-09-11 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_rename_createdate_drink_creation_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drink',
            old_name='desc',
            new_name='description',
        ),
    ]
