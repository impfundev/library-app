# Generated by Django 5.0.7 on 2024-07-17 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_alter_bookloan_book_alter_bookloan_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloan',
            name='loan_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
