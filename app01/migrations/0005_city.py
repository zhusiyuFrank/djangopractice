# Generated by Django 4.0.6 on 2022-08-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='城市名称')),
                ('count', models.IntegerField(verbose_name='人口')),
                ('img', models.FileField(max_length=128, upload_to='city/', verbose_name='Logo')),
            ],
        ),
    ]
