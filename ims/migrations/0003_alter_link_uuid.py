# Generated by Django 4.2.8 on 2023-12-14 17:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0002_link_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
