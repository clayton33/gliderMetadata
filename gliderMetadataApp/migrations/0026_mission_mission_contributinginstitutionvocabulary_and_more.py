# Generated by Django 4.1 on 2024-08-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gliderMetadataApp', '0025_remove_platformvariable_platform_variablestandardname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='mission_contributingInstitutionVocabulary',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_contributingInstitutions',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_contributingInstitutionsRole',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_contributingInstitutionsRoleVocabulary',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]