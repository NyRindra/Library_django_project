# Generated by Django 4.2 on 2023-05-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin_doc',
            field=models.BooleanField(default=False),
        ),
    ]
