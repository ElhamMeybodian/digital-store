# Generated by Django 4.2 on 2023-11-05 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import subscriptions.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="title")),
                (
                    "sku",
                    models.CharField(
                        db_index=True,
                        max_length=20,
                        validators=[subscriptions.validators.SKUValidator()],
                        verbose_name="stock keeping unit",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, upload_to="package/", verbose_name="avatar"
                    ),
                ),
                (
                    "is_enable",
                    models.BooleanField(default=True, verbose_name="is_enable"),
                ),
                ("price", models.PositiveIntegerField(verbose_name="price")),
                (
                    "duration",
                    models.DurationField(
                        blank=True, null=True, verbose_name="duration"
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created_time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(auto_now=True, verbose_name="updated_time"),
                ),
            ],
            options={
                "verbose_name": "Package",
                "verbose_name_plural": "Packages",
                "db_table": "packages",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created time"
                    ),
                ),
                (
                    "expire_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="expire time"
                    ),
                ),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="subscriptions.package",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
                "db_table": "subscriptions",
            },
        ),
    ]
