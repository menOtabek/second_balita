# Generated by Django 5.0.4 on 2024-04-16 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_comment_phone_remove_contact_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
