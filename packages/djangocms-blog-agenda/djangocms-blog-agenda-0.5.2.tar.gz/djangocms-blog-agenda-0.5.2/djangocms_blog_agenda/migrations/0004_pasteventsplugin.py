# Generated by Django 3.2.23 on 2023-12-12 08:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_blog", "0043_auto_20231212_0935"),
        ("djangocms_blog_agenda", "0003_upcomingeventsplugin"),
    ]

    operations = [
        migrations.CreateModel(
            name="PastEventsPlugin",
            fields=[],
            options={
                "verbose_name": "Past events plugin",
                "verbose_name_plural": "Past events plugins",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("djangocms_blog.latestpostsplugin",),
        ),
    ]
