# Generated by Django 3.0.7 on 2020-08-22 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_feeditem_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feeditem',
            old_name='picture',
            new_name='image',
        ),
    ]