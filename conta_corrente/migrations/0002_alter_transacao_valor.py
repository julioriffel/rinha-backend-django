# Generated by Django 5.0.2 on 2024-02-14 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conta_corrente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='valor',
            field=models.PositiveIntegerField(),
        ),
    ]
