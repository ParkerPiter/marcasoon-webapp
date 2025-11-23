from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_merge_20251114_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='trademark',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trademark',
            name='verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TrademarkVerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('trademark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_codes', to='core.trademark')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trademark_verification_codes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [
                    models.Index(fields=['user', 'code'], name='core_tradem_user_id_idx'),
                    models.Index(fields=['expires_at'], name='core_tradem_expires_idx'),
                ],
            },
        ),
    ]
