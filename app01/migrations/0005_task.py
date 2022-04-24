# Generated by Django 2.2.5 on 2022-04-24 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(3, '临时'), (2, '常规'), (1, '紧急')], default=2, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.CharField(max_length=100, verbose_name='详细信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Admin', verbose_name='负责人')),
            ],
        ),
    ]
