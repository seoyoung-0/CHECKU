# Generated by Django 2.0.13 on 2020-12-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subscription_list', models.CharField(choices=[('AC', 'Academic'), ('ST', 'Student'), ('SC', 'Scolarship'), ('IN', 'Industry'), ('EM', 'Employment'), ('CV', 'Corona'), ('IT', 'International')], max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='notice',
            name='subscribed',
            field=models.ManyToManyField(to='users.User'),
        ),
    ]
