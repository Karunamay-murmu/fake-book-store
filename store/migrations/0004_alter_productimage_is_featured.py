# Generated by Django 3.2.6 on 2021-09-14 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210913_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]