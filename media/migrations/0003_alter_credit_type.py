# Generated by Django 4.1.7 on 2023-03-30 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_alter_credit_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='type',
            field=models.CharField(choices=[('crew', 'crew'), ('cast', 'cast')], max_length=4, verbose_name='type'),
        ),
    ]
