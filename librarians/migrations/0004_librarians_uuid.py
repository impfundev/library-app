# Generated by Django 5.0.6 on 2024-07-10 10:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarians', '0003_alter_loginhistory_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarians',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c55123c4-cc13-4ce9-910a-559e026448d8')),
        ),
    ]
