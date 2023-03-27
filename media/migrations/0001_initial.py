# Generated by Django 4.1.7 on 2023-03-27 15:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('role', models.CharField(max_length=128, verbose_name='role')),
            ],
            options={
                'unique_together': {('name', 'role')},
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=32, verbose_name='name')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='title')),
                ('air_date', models.DateField(blank=True, null=True, verbose_name='air date')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=8, null=True, verbose_name='country')),
                ('credits', models.ManyToManyField(to='media.credit')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('tags', models.ManyToManyField(to='media.tag')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='sort title')),
                ('alternate_title', models.CharField(blank=True, max_length=256, null=True, verbose_name='alternate title')),
                ('premiere_date', models.DateField(blank=True, null=True, verbose_name='premiere date')),
                ('network', models.CharField(blank=True, max_length=56, null=True, verbose_name='network')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=8, null=True, verbose_name='country')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('tags', models.ManyToManyField(to='media.tag')),
            ],
            options={
                'verbose_name': 'show',
                'verbose_name_plural': 'shows',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media.show')),
            ],
            options={
                'verbose_name': 'season',
                'verbose_name_plural': 'seasons',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='sort title')),
                ('alternate_title', models.CharField(blank=True, max_length=256, null=True, verbose_name='alternate title')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='release date')),
                ('studio', models.CharField(blank=True, max_length=128, null=True, verbose_name='studio')),
                ('movie_rating', models.CharField(choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'), ('X', 'X')], max_length=8, verbose_name='movie rating')),
                ('tagline', models.TextField(blank=True, null=True, verbose_name='tagline')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=8, null=True, verbose_name='country')),
                ('credits', models.ManyToManyField(to='media.credit')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('library', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.movielibrary')),
                ('tags', models.ManyToManyField(to='media.tag')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='title')),
                ('air_date', models.DateField(blank=True, null=True, verbose_name='air date')),
                ('tv_audience_label', models.CharField(blank=True, choices=[('Y', 'Y'), ('Y7', 'Y7'), ('G', 'G'), ('PG', 'PG'), ('14', '14'), ('MA', 'MA')], max_length=8, null=True)),
                ('tv_content_label', models.CharField(blank=True, choices=[('D', 'D'), ('L', 'L'), ('S', 'S'), ('V', 'V'), ('AC', 'AC'), ('AL', 'AL'), ('GL', 'GL'), ('MV', 'MV'), ('GV', 'GV'), ('BN', 'BN'), ('N', 'N'), ('SSC', 'SSC'), ('RP', 'RP')], max_length=8, null=True)),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('credits', models.ManyToManyField(to='media.credit')),
            ],
            options={
                'verbose_name': 'episode',
                'verbose_name_plural': 'episodes',
            },
        ),
    ]
