# Generated by Django 4.0.6 on 2022-07-31 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_variation'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
