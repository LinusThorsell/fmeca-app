# Generated by Django 4.1.1 on 2022-09-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_node_nodefailure_partitionfailure_delete_subsystem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='material_group',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='nodefailure',
            name='comments',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='aircraft_level_effect',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='category',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='comments',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='criticality',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='event',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='failure_mode_effect',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='mission',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partitionfailure',
            name='subsystem_effect',
            field=models.TextField(default='', max_length=100),
        ),
    ]
