# Generated by Django 4.1.7 on 2023-03-20 19:44

from django.db import migrations, models
import home.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='', validators=[home.validators.validate_file_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
