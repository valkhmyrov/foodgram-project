# Generated by Django 3.1.6 on 2021-02-28 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0005_auto_20210227_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=1, help_text='Изображение', upload_to='foodgram_images/', verbose_name='Изображение'),
            preserve_default=False,
        ),
    ]