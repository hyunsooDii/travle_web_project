# Generated by Django 3.1 on 2020-08-25 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0008_delete_countryattachfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={},
        ),
        migrations.RemoveField(
            model_name='country',
            name='create_dt',
        ),
        migrations.RemoveField(
            model_name='country',
            name='modify_dt',
        ),
        migrations.RemoveField(
            model_name='country',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='country',
            name='tags',
        ),
        migrations.AlterModelTable(
            name='country',
            table=None,
        ),
    ]
