# Generated by Django 4.2.4 on 2023-08-31 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='link',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='ссылка'),
        ),
    ]
