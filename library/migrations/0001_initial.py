# Generated by Django 4.1.7 on 2023-04-05 22:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieLibrary',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(default='MyLibrary', max_length=128, verbose_name='name')),
                ('folder', models.CharField(max_length=1024, null=True, verbose_name='folder')),
                ('cover_photo', models.CharField(blank=True, max_length=128, null=True, verbose_name='cover photo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShowLibrary',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(default='MyLibrary', max_length=128, verbose_name='name')),
                ('folder', models.CharField(max_length=1024, null=True, verbose_name='folder')),
                ('cover_photo', models.CharField(blank=True, max_length=128, null=True, verbose_name='cover photo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoLibrary',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(default='MyLibrary', max_length=128, verbose_name='name')),
                ('folder', models.CharField(max_length=1024, null=True, verbose_name='folder')),
                ('cover_photo', models.CharField(blank=True, max_length=128, null=True, verbose_name='cover photo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
