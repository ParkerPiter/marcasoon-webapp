from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_add_trademark_and_user_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_codes', to='core.user')),
            ],
        ),
        migrations.AddIndex(
            model_name='passwordresetcode',
            index=models.Index(fields=['user', 'code'], name='core_passwo_user_id_c14b3d_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresetcode',
            index=models.Index(fields=['expires_at'], name='core_passwo_expires__2a86b8_idx'),
        ),
    ]
