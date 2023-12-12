# Generated by Django 3.2.18 on 2023-03-30 11:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("djangocms_blog_agenda", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postextension",
            options={
                "verbose_name": "Event infos",
                "verbose_name_plural": "Events infos",
            },
        ),
        migrations.RenameField(
            model_name="postextension",
            old_name="event_date",
            new_name="event_start_date",
        ),
        migrations.AddField(
            model_name="postextension",
            name="event_end_date",
            field=models.DateTimeField(
                blank=True,
                help_text="If the event is held over several days",
                null=True,
                verbose_name="Event end",
            ),
        ),
        migrations.AlterField(
            model_name="postextension",
            name="event_start_date",
            field=models.DateTimeField(verbose_name="Event start"),
        ),
    ]
