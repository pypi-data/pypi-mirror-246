# Generated by Django 2.2.28 on 2022-05-25 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processlib', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityinstance',
            name='assigned_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='assigned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='predecessors',
            field=models.ManyToManyField(blank=True, related_name='successors', to='processlib.ActivityInstance'),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityinstance',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
