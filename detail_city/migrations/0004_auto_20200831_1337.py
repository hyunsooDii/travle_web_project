# Generated by Django 3.1 on 2020-08-31 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detail_city', '0003_auto_20200826_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail_city',
            name='latitude',
            field=models.FloatField(max_length=200, null=True, verbose_name='LATITUDE'),
        ),
        migrations.AddField(
            model_name='detail_city',
            name='longitude',
            field=models.FloatField(max_length=200, null=True, verbose_name='LONGITUDE'),
        ),
    ]
