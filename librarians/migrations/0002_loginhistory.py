# Generated by Django 4.2 on 2024-06-26 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('librarians', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_at', models.DateTimeField(auto_now_add=True)),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarians.librarians')),
            ],
        ),
    ]
