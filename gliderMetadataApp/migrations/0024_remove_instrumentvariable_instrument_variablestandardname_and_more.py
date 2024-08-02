# Generated by Django 4.1 on 2024-07-31 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0023_remove_variable_variable_nercunit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrumentvariable',
            name='instrument_variableStandardName',
        ),
        migrations.AddField(
            model_name='instrumentvariable',
            name='instrument_cfVariable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.variablecfstandard'),
        ),
        migrations.AddField(
            model_name='instrumentvariable',
            name='instrument_nercVariable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.variablenercstandard'),
        ),
    ]