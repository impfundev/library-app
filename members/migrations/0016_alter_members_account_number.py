# Generated by Django 5.0.6 on 2024-07-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_alter_members_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='account_number',
            field=models.CharField(default='473840282244567', editable=False, max_length=15),
        ),
    ]
