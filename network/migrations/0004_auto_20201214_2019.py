# Generated by Django 3.1.2 on 2020-12-14 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20201214_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
