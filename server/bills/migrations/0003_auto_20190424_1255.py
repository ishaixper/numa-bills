# Generated by Django 2.2 on 2019-04-24 09:55

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20190407_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='features',
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='bill',
            name='image_id',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill',
            name='is_coin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bill',
            name='back',
            field=models.ImageField(upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='front',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
