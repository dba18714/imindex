# Generated by Django 5.0 on 2023-12-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0008_alter_link_description_alter_link_is_valid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('group', 'Group'), ('channel', 'Channel'), ('personal', 'Personal')], default='unknown', max_length=10),
        ),
        migrations.AlterField(
            model_name='link',
            name='is_valid',
            field=models.BooleanField(default=False, verbose_name='有效的'),
        ),
    ]
