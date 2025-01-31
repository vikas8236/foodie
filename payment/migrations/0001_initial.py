# Generated by Django 4.2.1 on 2024-08-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_payment_intent_id', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('currency', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('requires_payment_method', 'Requires Payment Method'), ('requires_confirmation', 'Requires Confirmation'), ('requires_action', 'Requires Action'), ('processing', 'Processing'), ('requires_capture', 'Requires Capture'), ('canceled', 'Canceled'), ('succeeded', 'Succeeded')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
