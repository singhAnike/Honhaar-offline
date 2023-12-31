# Generated by Django 4.2.2 on 2023-07-01 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('honhaarpannel', '0006_rename_question_question_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='topic_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='topic_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='standard',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='device_id',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='StudentQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField()),
                ('duration', models.FloatField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='honhaarpannel.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='honhaarpannel.student')),
            ],
            options={
                'unique_together': {('student', 'question')},
            },
        ),
    ]
