# Generated by Django 3.0.3 on 2020-02-24 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_offices'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=64, verbose_name='host name')),
                ('ip_address', models.CharField(max_length=16, verbose_name='ip_address')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Offices')),
            ],
            options={
                'verbose_name': 'Work Station',
                'verbose_name_plural': 'Work Stations',
            },
        ),
    ]