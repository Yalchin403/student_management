# Generated by Django 3.0.7 on 2021-03-15 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0010_auto_20210315_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.Subjects'),
        ),
    ]