# Generated by Django 5.0.3 on 2025-06-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statements', '0005_statement_unique_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(db_index=True, max_length=256),
        ),
    ]
