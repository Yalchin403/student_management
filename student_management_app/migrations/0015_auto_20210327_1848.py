# Generated by Django 3.0.7 on 2021-03-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0014_students_course_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='students',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='course_id',
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
        migrations.AddField(
            model_name='staffs',
            name='group_id',
            field=models.ManyToManyField(to='student_management_app.Group'),
        ),
        migrations.AddField(
            model_name='students',
            name='group_id',
            field=models.ManyToManyField(to='student_management_app.Group'),
        ),
    ]