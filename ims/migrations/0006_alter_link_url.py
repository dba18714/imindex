from django.db import migrations, models


def clean_duplicate_urls(apps, schema_editor):
    Link = apps.get_model('ims', 'Link')  # 替换 'ims' 和 'Link' 为你的应用名和模型名
    duplicates = Link.objects.values('url').annotate(
        url_count=models.Count('id')).filter(url_count__gt=1)

    for duplicate in duplicates:
        # 获取重复 URL 的所有对象
        duplicate_links = Link.objects.filter(url=duplicate['url'])
        # 保留一个，删除其他的
        for link in duplicate_links[1:]:
            link.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ims', '0005_link_member_count_alter_link_verified_at'),
    ]

    operations = [
        migrations.RunPython(clean_duplicate_urls, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
