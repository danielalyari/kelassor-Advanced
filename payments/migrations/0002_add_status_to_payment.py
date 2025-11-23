# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'در انتظار'),
                    ('paid', 'پرداخت شده'),
                    ('failed', 'ناموفق'),
                    ('refunded', 'برگشت داده شده'),
                ],
                default='pending',
                max_length=20
            ),
        ),
    ]

