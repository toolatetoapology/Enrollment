# Generated by Django 2.2.6 on 2019-11-18 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampusModel', '0005_delete_student_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_select',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=2)),
                ('cid', models.ForeignKey(on_delete='CASCADE', to='CampusModel.course')),
                ('sid', models.ForeignKey(on_delete='CASCADE', to='CampusModel.student')),
            ],
        ),
    ]
