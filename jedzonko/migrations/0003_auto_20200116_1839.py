# Generated by Django 2.2.6 on 2020-01-16 17:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jedzonko.models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(jedzonko.models.DayNames('Poniedziałek'), 'Poniedziałek'), (jedzonko.models.DayNames('Wtorek'), 'Wtorek'), (jedzonko.models.DayNames('Środa'), 'Środa'), (jedzonko.models.DayNames('Czwartek'), 'Czwartek'), (jedzonko.models.DayNames('Piątek'), 'Piątek'), (jedzonko.models.DayNames('Sobota'), 'Sobota'), (jedzonko.models.DayNames('Niedziela'), 'Niedziela')], max_length=32)),
                ('order', models.SmallIntegerField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RecipePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.IntegerField(choices=[(1, 'śniadanie'), (2, 'drugie śniadanie'), (3, 'obiad'), (4, 'podwieczorek'), (5, 'kolacja')])),
                ('order', models.SmallIntegerField()),
                ('day_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.DayName')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Plan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.RecipePlan', to='jedzonko.Recipe'),
        ),
    ]
