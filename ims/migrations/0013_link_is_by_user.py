# Generated by Django 5.0.3 on 2024-03-04 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0012_alter_link_category_alter_link_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='is_by_user',
            field=models.BooleanField(default=False, verbose_name='是否是用户提交的链接'),
        ),
    ]