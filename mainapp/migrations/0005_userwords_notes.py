# Generated by Django 2.0.5 on 2018-06-01 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20180601_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwords',
            name='notes',
            field=models.CharField(default='char', max_length=200),
        ),
    ]
