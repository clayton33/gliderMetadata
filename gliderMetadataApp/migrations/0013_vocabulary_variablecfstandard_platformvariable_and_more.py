# Generated by Django 4.1 on 2023-07-21 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0012_alter_mission_mission_comments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vocabulary', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VariableCFStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_standardName', models.CharField(max_length=100)),
                ('variable_longName', models.CharField(max_length=100)),
                ('variable_units', models.CharField(max_length=50)),
                ('variable_nameVocabulary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.vocabulary')),
            ],
        ),
        migrations.CreateModel(
            name='PlatformVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_variableSourceName', models.CharField(max_length=50)),
                ('platform_variableSourceUnits', models.CharField(max_length=50, null=True)),
                ('platform_variablePlatformCompany', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.platformcompany')),
                ('platform_variableStandardCF', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.variablecfstandard')),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_variableSourceName', models.CharField(max_length=50)),
                ('instrument_variableSourceUnits', models.CharField(max_length=50, null=True)),
                ('instrument_variableInstrumentModel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumentmodel')),
                ('instrument_variablePlatformCompany', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.platformcompany')),
                ('instrument_variableStandardCF', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.variablecfstandard')),
            ],
        ),
    ]
