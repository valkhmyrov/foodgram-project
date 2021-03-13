# Generated by Django 3.1.6 on 2021-02-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0003_auto_20210227_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tag',
        ),
        migrations.AddField(
            model_name='tag',
            name='checkbox_style',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='title',
            field=models.CharField(default=1, max_length=30, unique=True, verbose_name='Наименование тега'),
            preserve_default=False,
        ),
    ]