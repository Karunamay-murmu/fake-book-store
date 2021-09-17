# Generated by Django 3.2.6 on 2021-09-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, default='109.99', error_messages={'name': {'max_length': 'The price must be between 0 and 999.99'}}, help_text='maximum 999.99', max_digits=10, verbose_name='regular price'),
        ),
    ]
