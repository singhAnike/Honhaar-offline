# Generated by Django 4.2.2 on 2023-06-22 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honhaarpannel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_one_introduction', models.FileField(blank=True, null=True, upload_to='')),
                ('round_one_sponsor', models.FileField(blank=True, null=True, upload_to='')),
                ('round_one_instruction', models.FileField(blank=True, null=True, upload_to='')),
                ('round_two_introduction', models.FileField(blank=True, null=True, upload_to='')),
                ('round_two_sponsor', models.FileField(blank=True, null=True, upload_to='')),
                ('round_two_instruction', models.FileField(blank=True, null=True, upload_to='')),
                ('round_three_introduction', models.FileField(blank=True, null=True, upload_to='')),
                ('round_three_sponsor', models.FileField(blank=True, null=True, upload_to='')),
                ('round_three_instruction', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]