# Generated by Django 4.1 on 2023-05-09 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0008_mission'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentmission',
            name='instrument_mission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gliderMetadataApp.mission'),
        ),
    ]
