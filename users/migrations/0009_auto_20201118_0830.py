# Generated by Django 3.1.3 on 2020-11-18 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employer_companies', '0001_initial'),
        ('insurance_companies', '0001_initial'),
        ('users', '0008_auto_20201118_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employer_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employees', to='employer_companies.employercompany'),
        ),
        migrations.AlterField(
            model_name='user',
            name='insurance_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', related_query_name='clients', to='insurance_companies.insurancecompany'),
        ),
    ]
