# Generated by Django 5.0 on 2024-01-13 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(db_index=True, max_length=1024)),
                ('transaction_date', models.DateField()),
                ('amount_deposited', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('amount_withdrawn', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('others', models.TextField(null=True)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statements.statement')),
            ],
        ),
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.UniqueConstraint(fields=('statement_id', 'transaction_id'), name='unique-transaction-for-statement'),
        ),
    ]
