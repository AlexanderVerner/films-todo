import logging
from envjson import env_str
from django.db import migrations

logger = logging.getLogger(__name__)

def generate_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model

    username = env_str("ADMIN_USERNAME")
    password = env_str("ADMIN_PASSWORD")
    email = env_str("ADMIN_EMAIL")

    user = get_user_model()

    if not user.objects.filter(username=username, email=email).exists():
        logger.info("Creating new superuser")
        admin = user.objects.create_superuser(
           username=username, password=password, email=email
        )
        admin.save()
    else:
        logger.info("Superuser already created!")


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser)
    ]
