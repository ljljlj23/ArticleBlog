# Generated by Django 2.2.1 on 2019-09-16 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0004_auto_20190916_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='click',
            field=models.IntegerField(default=0, verbose_name='点击率'),
        ),
        migrations.AddField(
            model_name='article',
            name='recommend',
            field=models.IntegerField(default=0, verbose_name='推荐'),
        ),
    ]
