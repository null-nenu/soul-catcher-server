# Generated by Django 3.1.2 on 2020-10-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_auto_20201024_0716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slogan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
    ]
