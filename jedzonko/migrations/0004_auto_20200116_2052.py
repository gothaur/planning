# Generated by Django 2.2.6 on 2020-01-16 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0003_auto_20200116_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='day',
            field=models.CharField(choices=[('MON', 'Poniedziałek'), ('TUE', 'Wtorek'), ('WED', 'Środa'), ('THU', 'Czwartek'), ('FRI', 'Piątek'), ('SAT', 'Sobota'), ('SUN', 'Niedziela')], max_length=32),
        ),
    ]
