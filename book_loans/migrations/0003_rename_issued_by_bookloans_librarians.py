# Generated by Django 4.2 on 2024-06-26 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_loans', '0002_alter_bookloans_book_alter_bookloans_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookloans',
            old_name='issued_by',
            new_name='librarians',
        ),
    ]
