# Generated by Django 4.2.11 on 2024-04-26 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.CharField(max_length=20, unique=True)),
                ('category_name', models.CharField(max_length=200)),
                ('category_order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pool_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_id', models.CharField(max_length=20, unique=True)),
                ('subcategory_name', models.CharField(max_length=200)),
                ('subcategory_order', models.IntegerField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.CharField(max_length=20)),
                ('question_text', models.CharField(max_length=200)),
                ('answer_0', models.CharField(max_length=200)),
                ('answer_1', models.CharField(max_length=200)),
                ('answer_2', models.CharField(max_length=200)),
                ('answer_3', models.CharField(max_length=200)),
                ('solution', models.IntegerField()),
                ('outdated', models.BooleanField()),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pool')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subcategory')),
            ],
        ),
    ]
