# Generated by Django 5.0.4 on 2024-10-05 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0016_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='data/upload_file/'),
        ),
        migrations.AddField(
            model_name='ad',
            name='place',
            field=models.SmallIntegerField(choices=[(1, '首页'), (2, '详情页')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='url',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='start_at',
            field=models.DateTimeField(),
        ),
    ]