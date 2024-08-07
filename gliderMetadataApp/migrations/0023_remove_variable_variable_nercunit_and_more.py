# Generated by Django 4.1 on 2024-07-31 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0022_rename_calibrationseabird43f_calibration_instrumentseabird43foxygencalibrationcoefficients_calibrati'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variable',
            name='variable_nercUnit',
        ),
        migrations.RemoveField(
            model_name='variablenercstandard',
            name='variable_nameVocabulary',
        ),
        migrations.RemoveField(
            model_name='variablenercstandard',
            name='variable_standardNameUri',
        ),
        migrations.RemoveField(
            model_name='variablenercstandard',
            name='variable_standardNameUrn',
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_unit',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_unitLongName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_unitVocabulary',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_variableLongName',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_variableName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='variablenercstandard',
            name='variable_nerc_variableVocabulary',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='UnitNERCStandard',
        ),
    ]
