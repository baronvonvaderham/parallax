# Generated by Django 4.1.7 on 2023-04-05 18:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('languages_plus', '0004_auto_20171214_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('remote_access', models.BooleanField(default=True, verbose_name='remote access')),
                ('public_port', models.IntegerField(default=2500, verbose_name='public port')),
                ('upload_limit', models.IntegerField(default=10, verbose_name='upload limit')),
                ('scan_automatically', models.BooleanField(default=True, verbose_name='scan automatically')),
                ('changes_detected_scan', models.BooleanField(default=True, verbose_name='changes detected scan')),
                ('scheduled_scan_enabled', models.BooleanField(default=False, verbose_name='scheduled scan enabled')),
                ('scheduled_scan_interval', models.IntegerField(default=60, verbose_name='scheduled scan interval')),
                ('empty_trash_after_scan', models.BooleanField(default=True, verbose_name='empty trash after scan')),
                ('allow_delete', models.BooleanField(default=True, verbose_name='allow delete')),
                ('queue_retention_interval', models.IntegerField(default=28, verbose_name='queue retention interval')),
                ('max_queue_size', models.IntegerField(default=30, verbose_name='max queue size')),
                ('played_threshold', models.IntegerField(default=90, verbose_name='played threshold')),
                ('paused_termination_limit', models.IntegerField(default=10, verbose_name='paused termination limit')),
                ('max_stream_count', models.IntegerField(default=-1, verbose_name='max stream count')),
                ('transcoding_enabled', models.BooleanField(default=True, verbose_name='transcoding enabled')),
                ('max_transcode_count', models.IntegerField(default=-1, verbose_name='max transcode count')),
                ('authorized_users', models.ManyToManyField(related_name='authorized_users', to='core.user')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owner', to='core.user')),
                ('preferred_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='languages_plus.language')),
            ],
            options={
                'verbose_name': 'server',
                'verbose_name_plural': 'servers',
            },
        ),
    ]
