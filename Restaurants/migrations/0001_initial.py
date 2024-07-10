# Generated by Django 5.0.6 on 2024-07-09 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resImage', models.URLField(max_length=1000, null=True)),
                ('resName', models.CharField(max_length=200)),
                ('estimated_time', models.CharField(default='30-40 min', max_length=20)),
                ('menue', models.CharField(max_length=500)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('locality', models.CharField(default='VijayNagar Indore', max_length=500)),
                ('offer', models.CharField(default='50% aboove ₹199', max_length=500)),
            ],
        ),
    ]
