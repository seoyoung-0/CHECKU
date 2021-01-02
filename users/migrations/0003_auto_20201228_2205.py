# Generated by Django 2.0.13 on 2020-12-28 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20201228_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subscription_list', multiselectfield.db.fields.MultiSelectField(choices=[('AC', 'Academic'), ('ST', 'Student'), ('SC', 'Scolarship'), ('IN', 'Industry'), ('EM', 'Employment'), ('CV', 'Corona'), ('IT', 'International')], max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='notice',
            name='subscribed',
            field=models.ManyToManyField(to='users.MyUser'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
