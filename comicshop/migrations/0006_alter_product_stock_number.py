# Generated by Django 5.1.6 on 2025-03-08 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comicshop', '0005_alter_product_stock_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_number',
            field=models.CharField(max_length=6, verbose_name='Pg9P4R'),
        ),
    ]
