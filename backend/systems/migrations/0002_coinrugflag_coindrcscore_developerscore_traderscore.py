# Generated by Django 5.1.6 on 2025-05-06 11:22

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinRugFlag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_rugged', models.BooleanField(default=False)),
                ('rugged_at', models.DateTimeField(blank=True, null=True)),
                ('rug_transaction', models.UUIDField(blank=True, null=True)),
                ('rug_description', models.TextField(blank=True)),
                ('coin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rug_flag', to='systems.coin')),
            ],
        ),
        migrations.CreateModel(
            name='CoinDRCScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=200, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('holders_count', models.IntegerField(default=0)),
                ('age_in_hours', models.IntegerField(default=0)),
                ('trade_volume_24h', models.DecimalField(decimal_places=8, default=0, max_digits=24)),
                ('price_stability_score', models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('verified_contract', models.BooleanField(default=False)),
                ('audit_completed', models.BooleanField(default=False)),
                ('audit_score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('coin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='drc_score', to='systems.coin')),
            ],
            options={
                'indexes': [models.Index(fields=['score'], name='systems_coi_score_24d8d0_idx'), models.Index(fields=['coin'], name='systems_coi_coin_id_627fd1_idx'), models.Index(fields=['age_in_hours'], name='systems_coi_age_in__91a67b_idx')],
            },
        ),
        migrations.CreateModel(
            name='DeveloperScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=200, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('coins_created_count', models.IntegerField(default=0)),
                ('coins_active_24h_plus', models.IntegerField(default=0)),
                ('coins_rugged_count', models.IntegerField(default=0)),
                ('highest_market_cap', models.DecimalField(decimal_places=8, default=0, max_digits=24)),
                ('developer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='developer_score', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['score'], name='systems_dev_score_7a105e_idx'), models.Index(fields=['developer'], name='systems_dev_develop_bf4dcf_idx')],
            },
        ),
        migrations.CreateModel(
            name='TraderScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=200, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('coins_held_count', models.IntegerField(default=0)),
                ('avg_holding_time_hours', models.IntegerField(default=0)),
                ('trades_count', models.IntegerField(default=0)),
                ('quick_dumps_count', models.IntegerField(default=0)),
                ('profitable_trades_percent', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('trader', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trader_score', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['score'], name='systems_tra_score_746e5e_idx'), models.Index(fields=['trader'], name='systems_tra_trader__bc6d0b_idx')],
            },
        ),
    ]
