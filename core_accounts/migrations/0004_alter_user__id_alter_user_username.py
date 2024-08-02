# Generated by Django 5.0.7 on 2024-07-28 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_accounts', '0003_user__id_alter_user_date_joined_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='_id',
            field=models.CharField(db_index=True, default='', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True),
        ),
    ]
