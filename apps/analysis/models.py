from django.db import models
from django.conf import settings
from apps.projects.models import Project, ProjectFile
import uuid


class AnalysisReport(models.Model):
    ANALYSIS_TYPES = [
        ('code_quality', 'Code Quality'),
        ('security', 'Security Scan'),
        ('performance', 'Performance Analysis'),
        ('test_coverage', 'Test Coverage'),
        ('dependency', 'Dependency Analysis'),
    ]
    
    STATUSES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='analysis_reports')
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    
    # Analysis results
    score = models.FloatField(null=True, blank=True)
    results = models.JSONField(default=dict)
    summary = models.TextField(blank=True)
    
    # Metadata
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.get_analysis_type_display()}"


class CodeQualityMetric(models.Model):
    report = models.ForeignKey(AnalysisReport, on_delete=models.CASCADE, related_name='quality_metrics')
    file = models.ForeignKey(ProjectFile, on_delete=models.CASCADE)
    
    # Code quality metrics
    cyclomatic_complexity = models.IntegerField(null=True, blank=True)
    maintainability_index = models.FloatField(null=True, blank=True)
    lines_of_code = models.IntegerField(null=True, blank=True)
    code_duplications = models.IntegerField(default=0)
    
    # Linting results
    lint_errors = models.IntegerField(default=0)
    lint_warnings = models.IntegerField(default=0)
    lint_info = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Metrics for {self.file.file_name}"


class SecurityIssue(models.Model):
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    report = models.ForeignKey(AnalysisReport, on_delete=models.CASCADE, related_name='security_issues')
    file = models.ForeignKey(ProjectFile, on_delete=models.CASCADE)
    
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    issue_type = models.CharField(max_length=100)
    description = models.TextField()
    line_number = models.IntegerField(null=True, blank=True)
    cwe_id = models.CharField(max_length=20, blank=True)
    
    # Resolution status
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.severity.upper()}: {self.issue_type}"


class PerformanceMetric(models.Model):
    report = models.ForeignKey(AnalysisReport, on_delete=models.CASCADE, related_name='performance_metrics')
    
    # Performance metrics
    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.BigIntegerField(null=True, blank=True)
    cpu_usage = models.FloatField(null=True, blank=True)
    
    # Test/benchmark details
    test_name = models.CharField(max_length=255)
    test_description = models.TextField(blank=True)
    iterations = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Performance: {self.test_name}"


class TestCoverage(models.Model):
    report = models.ForeignKey(AnalysisReport, on_delete=models.CASCADE, related_name='test_coverage')
    file = models.ForeignKey(ProjectFile, on_delete=models.CASCADE)
    
    # Coverage metrics
    line_coverage = models.FloatField()
    branch_coverage = models.FloatField(null=True, blank=True)
    function_coverage = models.FloatField(null=True, blank=True)
    
    # Coverage details
    covered_lines = models.IntegerField()
    total_lines = models.IntegerField()
    missing_lines = models.JSONField(default=list)
    
    def __str__(self):
        return f"Coverage for {self.file.file_name}: {self.line_coverage}%"
