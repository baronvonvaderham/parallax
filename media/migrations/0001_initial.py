# Generated by Django 4.2.8 on 2023-12-06 20:21

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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('role', models.CharField(max_length=128, verbose_name='role')),
                ('type', models.CharField(choices=[('crew', 'crew'), ('cast', 'cast')], max_length=4, verbose_name='type')),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.CharField(blank=True, max_length=1024, null=True, verbose_name='filepath')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='title')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='release date')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=8, null=True, verbose_name='country')),
                ('credits', models.ManyToManyField(to='media.credit')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='videos', to='library.videolibrary')),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.CharField(blank=True, max_length=1024, null=True, verbose_name='filepath')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='sort title')),
                ('alternate_title', models.CharField(blank=True, max_length=256, null=True, verbose_name='alternate title')),
                ('premiere_date', models.DateField(blank=True, null=True, verbose_name='premiere date')),
                ('network', models.CharField(blank=True, max_length=56, null=True, verbose_name='network')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=8, null=True, verbose_name='country')),
                ('tmdb_id', models.IntegerField(blank=True, null=True, verbose_name='tmdb_id')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shows', to='library.showlibrary')),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='number')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start date')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='media.show')),
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
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.CharField(blank=True, max_length=1024, null=True, verbose_name='filepath')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('sort_title', models.CharField(max_length=256, verbose_name='sort title')),
                ('alternate_title', models.CharField(blank=True, max_length=256, null=True, verbose_name='alternate title')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='release date')),
                ('studio', models.CharField(blank=True, max_length=128, null=True, verbose_name='studio')),
                ('movie_rating', models.CharField(blank=True, choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'), ('X', 'X')], max_length=8, null=True, verbose_name='movie rating')),
                ('tagline', models.TextField(blank=True, null=True, verbose_name='tagline')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='summary')),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('country', models.CharField(blank=True, max_length=56, null=True, verbose_name='country')),
                ('credits', models.ManyToManyField(to='media.credit')),
                ('genres', models.ManyToManyField(to='media.genre')),
                ('library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies', to='library.movielibrary')),
                ('tags', models.ManyToManyField(to='media.tag')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'tmdb',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.CharField(blank=True, max_length=1024, null=True, verbose_name='filepath')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='title')),
                ('air_date', models.DateField(blank=True, null=True, verbose_name='air date')),
                ('tv_audience_label', models.CharField(blank=True, choices=[('Y', 'Y'), ('Y7', 'Y7'), ('G', 'G'), ('PG', 'PG'), ('14', '14'), ('MA', 'MA')], max_length=8, null=True)),
                ('tv_content_label', models.CharField(blank=True, choices=[('D', 'D'), ('L', 'L'), ('S', 'S'), ('V', 'V'), ('AC', 'AC'), ('AL', 'AL'), ('GL', 'GL'), ('MV', 'MV'), ('GV', 'GV'), ('BN', 'BN'), ('N', 'N'), ('SSC', 'SSC'), ('RP', 'RP')], max_length=8, null=True)),
                ('poster_image', models.CharField(blank=True, max_length=128, null=True, verbose_name='poster image')),
                ('credits', models.ManyToManyField(to='media.credit')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='media.season')),
            ],
            options={
                'verbose_name': 'episode',
                'verbose_name_plural': 'episodes',
            },
        ),
    ]
