# Generated by Django 2.2.10 on 2020-04-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_auto_20200404_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='calendarOwnerTID',
            field=models.IntegerField(default=753176642, editable=False),
        ),
    ]
