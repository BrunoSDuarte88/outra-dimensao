# Generated by Django 5.2.3 on 2025-06-24 01:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='postagem',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postagens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topico',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topico',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to='forum.forum'),
        ),
        migrations.AddField(
            model_name='postagem',
            name='topico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postagens', to='forum.topico'),
        ),
    ]
