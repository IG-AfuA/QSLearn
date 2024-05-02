# Generated by Django 4.2.11 on 2024-05-02 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('app', '0002_question_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='When did user start the quiz?')),
                ('due_time', models.DateTimeField(blank=True, null=True, verbose_name='When is the quiz due?')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='When did the user hand in quiz?')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pool')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
            ],
        ),
    ]
