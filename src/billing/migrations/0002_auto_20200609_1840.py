# Generated by Django 3.0.4 on 2020-06-09 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingprofile',
            old_name='User',
            new_name='user',
        ),
    ]
