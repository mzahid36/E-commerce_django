# Generated by Django 4.2 on 2023-07-18 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_bannerimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('m', 'Man'), ('w', 'Woman'), ('k', 'Kids')], max_length=2),
        ),
    ]
