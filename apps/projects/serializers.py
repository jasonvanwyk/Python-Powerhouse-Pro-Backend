from rest_framework import serializers
from .models import Project, ProjectSettings, ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProjectSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSettings
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    settings = ProjectSettingsSerializer(read_only=True)
    files = ProjectFileSerializer(many=True, read_only=True)
    file_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at', 'last_accessed')
    
    def get_file_count(self, obj):
        return obj.files.count()
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        project = super().create(validated_data)
        ProjectSettings.objects.create(project=project)
        return project


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'root_path', 'git_repository', 'python_version', 'is_public')
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        project = super().create(validated_data)
        ProjectSettings.objects.create(project=project)
        return project