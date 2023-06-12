# Generated by Django 4.1.4 on 2023-05-22 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0005_alter_configuration_comment_alter_configuration_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurationlimitationparameter',
            name='configuration',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='limitation_configurations', to='teacher_app.configuration'),
            preserve_default=False,
        ),
    ]