from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from .models import Project, ProjectSettings, ProjectFile
from .serializers import ProjectSerializer, ProjectCreateSerializer, ProjectSettingsSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(owner=user) | models.Q(collaborators=user)
        ).distinct().order_by('-updated_at')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.last_accessed = timezone.now()
        instance.save(update_fields=['last_accessed'])
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['get', 'patch'])
    def settings(self, request, pk=None):
        project = self.get_object()
        settings, created = ProjectSettings.objects.get_or_create(project=project)
        
        if request.method == 'GET':
            serializer = ProjectSettingsSerializer(settings)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = ProjectSettingsSerializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        project = self.get_object()
        files = project.files.all()
        from .serializers import ProjectFileSerializer
        serializer = ProjectFileSerializer(files, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
            return Response({'error': 'Only project owner can add collaborators'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from apps.authentication.models import User
            user = User.objects.get(email=email)
            project.collaborators.add(user)
            return Response({'message': f'Added {email} as collaborator'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
