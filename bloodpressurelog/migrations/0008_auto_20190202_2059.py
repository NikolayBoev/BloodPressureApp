# Generated by Django 2.2.dev20180926065127 on 2019-02-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodpressurelog', '0007_statistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
