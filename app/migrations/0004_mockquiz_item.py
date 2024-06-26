# Generated by Django 4.2.11 on 2024-05-02 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_mockquiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockQuiz_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('submitted_answer', models.IntegerField(default=None, null=True)),
                ('correct_answer', models.IntegerField()),
                ('permutation', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mockquiz')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
            ],
        ),
    ]
