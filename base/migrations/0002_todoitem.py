# Generated by Django 4.1.5 on 2023-01-06 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(default='')),
                ('complete', models.BooleanField(default=False)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.task')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
    ]
