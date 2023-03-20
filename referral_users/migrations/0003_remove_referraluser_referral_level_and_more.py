# Generated by Django 4.1.7 on 2023-03-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_users', '0002_referraluser_bonuses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referraluser',
            name='referral_level',
        ),
        migrations.AddField(
            model_name='referraluser',
            name='level',
            field=models.CharField(choices=[('V1', 'V1'), ('V2', 'V2'), ('V3', 'V3'), ('V4', 'V4'), ('V5', 'V5'), ('V6', 'V6')], default='V1', max_length=2),
        ),
        migrations.DeleteModel(
            name='ReferralLevel',
        ),
    ]
