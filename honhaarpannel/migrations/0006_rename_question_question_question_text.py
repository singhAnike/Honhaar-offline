# Generated by Django 4.2.2 on 2023-06-23 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('honhaarpannel', '0005_rename_option_question_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='question_text',
        ),
    ]