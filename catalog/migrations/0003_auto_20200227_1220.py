# Generated by Django 3.0.3 on 2020-02-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200213_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='productscategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='productscategory',
            name='image',
            field=models.ImageField(default='../static/images/noimage.png', upload_to='categories/%Y/%m-%d', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='servicescategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='servicescategory',
            name='image',
            field=models.ImageField(default='../static/images/noimage.png', upload_to='categories/%Y/%m-%d', verbose_name='Image'),
        ),
    ]
