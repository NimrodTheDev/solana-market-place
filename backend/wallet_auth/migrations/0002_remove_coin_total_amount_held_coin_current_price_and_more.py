# Generated by Django 5.1.6 on 2025-03-19 06:04

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='total_amount_held',
        ),
        migrations.AddField(
            model_name='coin',
            name='current_price',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=20),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('trade_type', models.BooleanField()),
                ('coin_amount', models.DecimalField(decimal_places=8, max_digits=20)),
                ('sol_amount', models.DecimalField(decimal_places=8, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='wallet_auth.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserCoinHoldings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_held', models.DecimalField(decimal_places=8, default=0, max_digits=20)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holders', to='wallet_auth.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'coin')},
            },
        ),
    ]
