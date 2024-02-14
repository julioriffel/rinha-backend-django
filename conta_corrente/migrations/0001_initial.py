# Generated by Django 5.0.2 on 2024-02-13 12:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def initial_data():
    return ('INSERT INTO conta_corrente_cliente (id, limite, saldo) VALUES '
            '(1, 100000, 0),(2,80000,0),(3,1000000,0),(4,10000000,0),(5,500000,0);')


def roolback_data():
    return ('select 1;')


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite', models.PositiveIntegerField(default=0)),
                ('saldo', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('c', 'Credit'), ('d', 'Debit')], max_length=1)),
                ('valor', models.IntegerField()),
                ('descricao', models.CharField(max_length=10)),
                ('realizada_em', models.DateTimeField(default=django.utils.timezone.now)),
                (
                    'cliente',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conta_corrente.cliente')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.RunSQL(initial_data(), roolback_data())
    ]
