# Generated by Django 3.2 on 2021-05-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utils', '0008_rename_contact_contacts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
                ('alt', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='contacts',
            options={'verbose_name_plural': 'Contacts'},
        ),
    ]
