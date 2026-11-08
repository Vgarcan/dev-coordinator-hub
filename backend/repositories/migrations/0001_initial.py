# Initial Repository migration for the Django 5.2 LTS project.
# Keep model fields in sync with repositories/models.py.

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(message='Use GitHub owner/repository format.', regex='\\A[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\\Z')])),
                ('description', models.TextField(blank=True)),
                ('tracking_status', models.CharField(choices=[('candidate', 'Candidate'), ('tracked', 'Tracked'), ('archived', 'Archived')], default='candidate', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
    ]
