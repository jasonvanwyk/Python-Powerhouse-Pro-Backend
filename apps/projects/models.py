from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='collaborated_projects')
    
    # Project paths and structure
    root_path = models.TextField()
    git_repository = models.URLField(blank=True)
    
    # Project metadata
    python_version = models.CharField(max_length=20, blank=True)
    requirements_file = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    # Status and settings
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name


class ProjectSettings(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='settings')
    
    # Code analysis settings
    enable_linting = models.BooleanField(default=True)
    enable_type_checking = models.BooleanField(default=True)
    enable_security_scan = models.BooleanField(default=True)
    
    # Testing settings
    test_framework = models.CharField(max_length=50, default='pytest')
    test_directory = models.CharField(max_length=255, default='tests/')
    
    # Build settings
    build_command = models.TextField(blank=True)
    environment_variables = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Settings for {self.project.name}"


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file_path = models.TextField()
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField()
    
    # File metadata
    lines_of_code = models.IntegerField(null=True, blank=True)
    complexity_score = models.FloatField(null=True, blank=True)
    last_modified = models.DateTimeField()
    
    # Content hash for change detection
    content_hash = models.CharField(max_length=64)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['project', 'file_path']
        ordering = ['file_path']
    
    def __str__(self):
        return f"{self.project.name}/{self.file_path}"
