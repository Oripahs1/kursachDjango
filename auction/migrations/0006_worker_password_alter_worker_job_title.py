# Generated by Django 5.0.3 on 2024-03-14 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_rename_car_for_page_carforpage_car_auc_list_photocar'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='password',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='job_title',
            field=models.TextField(choices=[('Клиент-менеджер', 'Менеджер'), ('Логист', 'Уссурийс'), ('HR', 'HR'), ('Бухгалтер', 'Бухгалтер'), ('Оперативник', 'Оперативник')]),
        ),
    ]
