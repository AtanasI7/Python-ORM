# Generated by Django 5.0.4 on 2025-03-10 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_lectureprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LectureProfile',
            new_name='LecturerProfile',
        ),
    ]
