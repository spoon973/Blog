# Generated by Django 2.2.3 on 2020-07-13 12:31

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='其他', max_length=200, verbose_name='类名')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'db_table': 'FileCategory',
            },
        ),
        migrations.CreateModel(
            name='FileStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='文件名')),
                ('file', models.FileField(upload_to='File', verbose_name='文件')),
                ('floader_cate', models.CharField(choices=[('Z', 'zip'), ('T', 'txt'), ('PT', 'ppt'), ('PF', 'pdf'), ('W', 'word'), ('H', 'html'), ('O', 'other'), ('E', 'excel'), ('M', 'markdown')], default='O', max_length=2, verbose_name='文件类别')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transferfiles.Category', verbose_name='内容类别')),
            ],
            options={
                'verbose_name': '文件存储',
                'verbose_name_plural': '文件存储',
                'db_table': 'FileStore',
            },
        ),
    ]
