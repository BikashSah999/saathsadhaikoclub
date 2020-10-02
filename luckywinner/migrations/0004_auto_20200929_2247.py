# Generated by Django 3.0.6 on 2020-09-29 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('luckywinner', '0003_auto_20200929_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='luckydraw',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='participants',
            name='luckydraw',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='luckywinner.Luckydraw'),
        ),
    ]
