# Generated by Django 4.2.1 on 2023-05-07 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_at',
        ),
    ]
