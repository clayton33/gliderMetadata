# Generated by Django 4.1 on 2023-07-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0018_contributormission'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='mission_summary',
            field=models.CharField(max_length=1200, null=True),
        ),
    ]
