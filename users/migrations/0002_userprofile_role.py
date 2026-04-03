from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(
                choices=[
                    ('SUPER_ADMIN', 'Super Admin'),
                    ('ADMIN', 'Admin'),
                    ('REGISTERED_USER', 'Registered User'),
                    ('VIEWER', 'Viewer'),
                ],
                default='VIEWER',
                max_length=20,
            ),
        ),
    ]