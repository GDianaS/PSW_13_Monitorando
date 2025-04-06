# Generated by Django 5.1.7 on 2025-04-03 20:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorados', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorados',
            name='estagio',
            field=models.CharField(choices=[('E1', '10-100k'), ('E2', '100-500K'), ('E3', '500-1000K'), ('E4', '1000-2000K')], max_length=2),
        ),
        migrations.CreateModel(
            name='DisponibilidadedeHorarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicial', models.DateTimeField(blank=True, null=True)),
                ('agendado', models.BooleanField(default=False)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
