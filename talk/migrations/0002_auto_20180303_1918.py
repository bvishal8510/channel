# Generated by Django 2.0.2 on 2018-03-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='room',
            field=models.IntegerField(default=1),
        ),
    ]
