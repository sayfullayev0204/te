# Generated by Django 5.2.4 on 2025-07-18 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessmentcriteria',
            options={'verbose_name': 'Baholash mezoni', 'verbose_name_plural': 'Baholash mezonlari'},
        ),
        migrations.AlterModelOptions(
            name='coursematerial',
            options={'ordering': ['material_type', 'order', 'title'], 'verbose_name': "Fan ma'lumoti", 'verbose_name_plural': "Fan ma'lumotlari"},
        ),
        migrations.AlterModelOptions(
            name='regulatorydocument',
            options={'ordering': ['document_type', 'title'], 'verbose_name': 'Meyoriy hujjat', 'verbose_name_plural': 'Meyoriy hujjatlar'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Fan', 'verbose_name_plural': 'Fanlar'},
        ),
        migrations.AlterModelOptions(
            name='userprogress',
            options={'verbose_name': 'Foydalanuvchi jarayoni', 'verbose_name_plural': 'Foydalanuvchi jarayonlari'},
        ),
        migrations.AddField(
            model_name='controltest',
            name='num_questions_to_display',
            field=models.IntegerField(default=20, help_text="Foydalanuvchiga ko'rsatiladigan savollar soni"),
        ),
        migrations.AlterField(
            model_name='controltest',
            name='total_questions',
            field=models.IntegerField(default=20, help_text='Test uchun mavjud savollar havzasining umumiy soni'),
        ),
    ]
