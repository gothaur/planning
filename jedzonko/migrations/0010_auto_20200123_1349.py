# Generated by Django 2.2.6 on 2020-01-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0009_auto_20200122_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeplan',
            name='order',
            field=models.SmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')]),
        ),
    ]