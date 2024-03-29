# Generated by Django 4.1.4 on 2022-12-13 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentCalibration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_calibrationDate', models.DateField(null=True)),
                ('instrument_calibrationReport', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_make', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_model', models.CharField(max_length=50)),
                ('instrument_longname', models.CharField(max_length=100)),
                ('instrument_modelMake', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumentmake')),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentSerialNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_serialNumber', models.CharField(max_length=20)),
                ('instrument_originalPlatform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.platformname')),
                ('instrument_serialNumberModel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumentmodel')),
            ],
        ),
        migrations.AddField(
            model_name='instrumentmodel',
            name='instrument_modelType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumenttype'),
        ),
        migrations.CreateModel(
            name='InstrumentMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument_warmUp', models.CharField(max_length=20)),
                ('instrument_samplingRate', models.CharField(max_length=20)),
                ('instrument_calibration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumentcalibration')),
            ],
        ),
        migrations.AddField(
            model_name='instrumentcalibration',
            name='instrument_calibrationSerial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.instrumentserialnumber'),
        ),
    ]
