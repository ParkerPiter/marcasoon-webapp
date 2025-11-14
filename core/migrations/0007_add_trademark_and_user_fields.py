# Generated migration to add intake fields and TrademarkEvidence
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_add_images_to_testimonial_blogpost'),
    ]

    operations = [
        # User fields
        migrations.AddField(
            model_name='user',
            name='nationality',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        # Trademark fields
        migrations.AddField(
            model_name='trademark',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='trademark',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='foreign_meaning',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='trademark',
            name='basis_for_registration',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='trademark',
            name='intention_of_use',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='current_use_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='first_use_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='foreign_application_number',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='trademark',
            name='foreign_application_translation',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='foreign_registration_number',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='trademark',
            name='foreign_registration_translation',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='trademark',
            name='disclaimer',
            field=models.TextField(blank=True),
        ),
        # TrademarkAsset fields
        migrations.AddField(
            model_name='trademarkasset',
            name='protect_colors',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trademarkasset',
            name='colors',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='trademarkasset',
            name='includes_person_name',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trademarkasset',
            name='person_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='trademarkasset',
            name='authorization',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='trademarkasset',
            name='services',
            field=models.TextField(blank=True),
        ),
        # Create TrademarkEvidence model
        migrations.CreateModel(
            name='TrademarkEvidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='evidence/')),
                ('links', models.JSONField(blank=True, default=list)),
                ('description', models.TextField(blank=True)),
                ('first_use_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trademark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidence', to='core.trademark')),
            ],
        ),
    ]
