# Generated by Django 5.0.3 on 2024-03-18 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0013_link_is_by_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='verified_start_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='验证开始时间'),
        ),
    ]
