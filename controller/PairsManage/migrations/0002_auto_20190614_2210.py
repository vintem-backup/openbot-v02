# Generated by Django 2.2.1 on 2019-06-15 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PairsManage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='binancepair',
            old_name='last_change_by_PID',
            new_name='last_change_by_pid',
        ),
        migrations.RemoveField(
            model_name='binancepair',
            name='last_stored_candle',
        ),
    ]