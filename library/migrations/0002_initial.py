# Generated by Django 4.1.7 on 2023-04-05 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0001_initial'),
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolibrary',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='server.server'),
        ),
        migrations.AddField(
            model_name='showlibrary',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='server.server'),
        ),
        migrations.AddField(
            model_name='movielibrary',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='server.server'),
        ),
    ]
