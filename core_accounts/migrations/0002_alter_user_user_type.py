# Generated by Django 5.0.7 on 2024-07-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')], default='', max_length=20, null=True),
        ),
    ]
