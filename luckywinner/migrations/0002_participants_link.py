# Generated by Django 3.0.6 on 2020-09-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckywinner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participants',
            name='link',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
