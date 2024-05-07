# Generated by Django 5.0.4 on 2024-05-05 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_picture_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture_content',
            field=models.ImageField(blank=True, default='aaaaa.jpg', null=True, upload_to='posts/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'gif', 'heif', 'jpg', 'webp'])]),
        ),
    ]
