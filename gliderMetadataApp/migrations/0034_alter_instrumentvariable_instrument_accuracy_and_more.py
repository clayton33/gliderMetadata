# Generated by Django 4.1 on 2024-10-23 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0033_instrumentvariable_instrument_accuracy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumentvariable',
            name='instrument_accuracy',
            field=models.DecimalField(decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentvariable',
            name='instrument_precision',
            field=models.DecimalField(decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentvariable',
            name='instrument_resolution',
            field=models.DecimalField(decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentvariable',
            name='instrument_validMax',
            field=models.DecimalField(decimal_places=6, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentvariable',
            name='instrument_validMin',
            field=models.DecimalField(decimal_places=6, max_digits=12, null=True),
        ),
    ]
