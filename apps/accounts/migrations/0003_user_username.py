# Generated by Django 4.2 on 2023-05-05 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(
                default="username", max_length=225, verbose_name="Username"
            ),
        ),
    ]
