# Generated by Django 4.1 on 2024-08-23 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0027_mission_mission_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributorrole',
            name='contributor_vocabulary',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
