# Generated by Django 3.0.3 on 2020-02-29 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200227_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='image',
            field=models.ImageField(default='../static/images/avatar/unnamed.jpg', upload_to='products/%Y/%m-%d', verbose_name='Image'),
        ),
    ]