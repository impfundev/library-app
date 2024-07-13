# Generated by Django 5.0.6 on 2024-07-12 03:10

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0026_remove_members_account_number_remove_members_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='members',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='members',
            name='user',
        ),
        migrations.AddField(
            model_name='members',
            name='account_number',
            field=models.CharField(default='867934046970059', editable=False, max_length=15),
        ),
        migrations.AddField(
            model_name='members',
            name='email',
            field=models.EmailField(default=datetime.datetime(2024, 7, 12, 3, 10, 8, 751856, tzinfo=datetime.timezone.utc), max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='members',
            name='name',
            field=models.CharField(default=datetime.datetime(2024, 7, 12, 3, 10, 12, 339105, tzinfo=datetime.timezone.utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='members',
            name='password',
            field=models.CharField(default=datetime.datetime(2024, 7, 12, 3, 10, 18, 879028, tzinfo=datetime.timezone.utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='members',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d369404f-1c7c-401d-835b-e5d6d097d77a')),
        ),
    ]
