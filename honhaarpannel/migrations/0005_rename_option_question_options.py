# Generated by Django 4.2.2 on 2023-06-23 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('honhaarpannel', '0004_alter_question_option'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='option',
            new_name='options',
        ),
    ]
