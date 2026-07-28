# Generated migration to fix JSONField default values

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_remove_movie_actors_photos_remove_movie_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='movie',
            name='countries',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='movie',
            name='directors',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='movie',
            name='watchability',
            field=models.JSONField(default=list, null=True),
        ),
    ]
