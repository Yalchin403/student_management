# Generated by Django 3.1.7 on 2021-04-11 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0017_auto_20210411_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.group'),
        ),
    ]
