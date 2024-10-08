# Generated by Django 5.0.6 on 2024-07-12 17:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_alter_account_balance_alter_account_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNo', models.IntegerField(null=True, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
