# Generated by Django 4.1 on 2024-08-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0028_alter_contributorrole_contributor_vocabulary'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentvariable',
            name='instrument_gmcdKeyword',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
