# Generated by Django 3.2.6 on 2021-09-13 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='payment ammont')),
                ('client_secret', models.CharField(max_length=255, null=True, verbose_name='client secret')),
                ('transaction_id', models.CharField(max_length=255, verbose_name='transaction id')),
                ('payment_intent', models.CharField(max_length=255, verbose_name='payment intent id')),
                ('payment_method', models.CharField(max_length=255, verbose_name='payment method id')),
                ('payment_type', models.CharField(max_length=25, verbose_name='payment type')),
                ('payment_created_at', models.PositiveIntegerField(verbose_name='payment create on')),
                ('currency_code', models.CharField(max_length=255, verbose_name='payment currency code')),
                ('card_brand', models.CharField(max_length=25, verbose_name='card brand')),
                ('card_country', models.CharField(max_length=25, verbose_name='card country')),
                ('card_last_4_digit', models.CharField(max_length=255, verbose_name='card last 4 digit')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]