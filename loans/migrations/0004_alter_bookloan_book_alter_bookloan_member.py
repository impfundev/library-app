# Generated by Django 5.0.7 on 2024-07-16 05:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_remove_book_category_book_category'),
        ('loans', '0003_bookloan_created_at_bookloan_updated_at'),
        ('users', '0003_alter_librarianloginhistory_librarian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloan',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book'),
        ),
        migrations.AlterField(
            model_name='bookloan',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.member'),
        ),
    ]
