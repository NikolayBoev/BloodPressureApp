# Generated by Django 2.2.dev20180926065127 on 2019-02-02 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodpressurelog', '0006_auto_20190202_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
                ('topNumber', models.FloatField()),
                ('bottomNumber', models.FloatField()),
                ('puls', models.FloatField()),
            ],
        ),
    ]
