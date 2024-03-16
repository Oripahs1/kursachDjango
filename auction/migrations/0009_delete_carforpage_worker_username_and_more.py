# Generated by Django 5.0.3 on 2024-03-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0008_alter_worker_full_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CarForPage',
        ),
        migrations.AddField(
            model_name='worker',
            name='username',
            field=models.TextField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='full_name',
            field=models.TextField(),
        ),
    ]
