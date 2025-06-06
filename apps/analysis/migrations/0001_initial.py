# Generated by Django 5.0.2 on 2025-06-05 14:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnalysisReport",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "analysis_type",
                    models.CharField(
                        choices=[
                            ("code_quality", "Code Quality"),
                            ("security", "Security Scan"),
                            ("performance", "Performance Analysis"),
                            ("test_coverage", "Test Coverage"),
                            ("dependency", "Dependency Analysis"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("score", models.FloatField(blank=True, null=True)),
                ("results", models.JSONField(default=dict)),
                ("summary", models.TextField(blank=True)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-started_at"],
            },
        ),
        migrations.CreateModel(
            name="CodeQualityMetric",
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
                ("cyclomatic_complexity", models.IntegerField(blank=True, null=True)),
                ("maintainability_index", models.FloatField(blank=True, null=True)),
                ("lines_of_code", models.IntegerField(blank=True, null=True)),
                ("code_duplications", models.IntegerField(default=0)),
                ("lint_errors", models.IntegerField(default=0)),
                ("lint_warnings", models.IntegerField(default=0)),
                ("lint_info", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="PerformanceMetric",
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
                ("execution_time", models.FloatField(blank=True, null=True)),
                ("memory_usage", models.BigIntegerField(blank=True, null=True)),
                ("cpu_usage", models.FloatField(blank=True, null=True)),
                ("test_name", models.CharField(max_length=255)),
                ("test_description", models.TextField(blank=True)),
                ("iterations", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="SecurityIssue",
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
                    "severity",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                            ("critical", "Critical"),
                        ],
                        max_length=10,
                    ),
                ),
                ("issue_type", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("line_number", models.IntegerField(blank=True, null=True)),
                ("cwe_id", models.CharField(blank=True, max_length=20)),
                ("is_resolved", models.BooleanField(default=False)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("resolution_notes", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="TestCoverage",
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
                ("line_coverage", models.FloatField()),
                ("branch_coverage", models.FloatField(blank=True, null=True)),
                ("function_coverage", models.FloatField(blank=True, null=True)),
                ("covered_lines", models.IntegerField()),
                ("total_lines", models.IntegerField()),
                ("missing_lines", models.JSONField(default=list)),
            ],
        ),
    ]
