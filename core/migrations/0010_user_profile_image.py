from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_trademark_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
