# Generated by Django 2.2.10 on 2020-04-04 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_auto_20200401_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='calendarOwnerTID',
            field=models.IntegerField(default=1247377096, editable=False),
        ),
    ]
