# Generated by Django 2.2.7 on 2019-11-28 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='uinfo_id',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='uid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.User'),
            preserve_default=False,
        ),
    ]