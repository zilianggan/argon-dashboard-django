# Generated by Django 3.2.6 on 2024-02-01 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmember',
            name='position',
            field=models.CharField(default='member', max_length=100),
            preserve_default=False,
        ),
    ]
