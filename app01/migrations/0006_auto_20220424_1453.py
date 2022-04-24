# Generated by Django 2.2.5 on 2022-04-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='detail',
            field=models.TextField(max_length=100, verbose_name='详细信息'),
        ),
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.SmallIntegerField(choices=[(2, '常规'), (3, '临时'), (1, '紧急')], default=2, verbose_name='级别'),
        ),
    ]