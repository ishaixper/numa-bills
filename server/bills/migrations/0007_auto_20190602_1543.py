# Generated by Django 2.2.1 on 2019-06-02 12:43

import bills.models.bill
import bills.models.detection
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_auto_20190529_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='back',
            field=models.ImageField(blank=True, upload_to=bills.models.bill.get_catalog_file_name),
        ),
        migrations.AlterField(
            model_name='bill',
            name='front',
            field=models.ImageField(blank=True, upload_to=bills.models.bill.get_catalog_file_name),
        ),
        migrations.AlterField(
            model_name='detection',
            name='back',
            field=models.ImageField(upload_to=bills.models.detection.get_detection_file_name),
        ),
        migrations.AlterField(
            model_name='detection',
            name='front',
            field=models.ImageField(upload_to=bills.models.detection.get_detection_file_name),
        ),
    ]
