# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Interlude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interludes', to='songs.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='songs.Artist')),
            ],
        ),
        migrations.AddField(
            model_name='interlude',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interludes', to='songs.Song'),
        ),
        migrations.AddField(
            model_name='episode',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='songs.Program'),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('name', 'artist')]),
        ),
        migrations.AlterUniqueTogether(
            name='interlude',
            unique_together=set([('song', 'order', 'episode')]),
        ),
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together=set([('program', 'date')]),
        ),
    ]
