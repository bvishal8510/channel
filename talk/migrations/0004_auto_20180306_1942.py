# Generated by Django 2.0.2 on 2018-03-06 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0003_auto_20180306_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('uploaded_at',)},
        ),
    ]
