# Generated by Django 3.0.5 on 2020-04-28 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0003_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='order_id',
            new_name='order',
        ),
    ]
