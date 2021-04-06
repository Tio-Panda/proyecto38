# Generated by Django 3.1.7 on 2021-03-29 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Negocios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('transbank', models.CharField(max_length=200)),
                ('efectivo', models.CharField(max_length=200)),
                ('cache', models.CharField(max_length=200)),
                ('dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='negocios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
