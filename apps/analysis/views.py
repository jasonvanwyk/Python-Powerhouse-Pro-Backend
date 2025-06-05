from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import AnalysisReport
from .serializers import AnalysisReportSerializer, AnalysisReportCreateSerializer


class AnalysisReportViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnalysisReport.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AnalysisReportCreateSerializer
        return AnalysisReportSerializer
    
    def get_queryset(self):
        user = self.request.user
        return AnalysisReport.objects.filter(
            project__owner=user
        ).order_by('-started_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start_analysis(self, request, pk=None):
        report = self.get_object()
        if report.status != 'pending':
            return Response({'error': 'Analysis already started or completed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        report.status = 'running'
        report.save()
        
        # Here you would trigger the actual analysis task
        # For now, we'll just simulate it
        return Response({'message': 'Analysis started'})
    
    @action(detail=True, methods=['post'])
    def complete_analysis(self, request, pk=None):
        report = self.get_object()
        if report.status != 'running':
            return Response({'error': 'Analysis not running'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        report.status = 'completed'
        report.completed_at = timezone.now()
        report.save()
        
        return Response({'message': 'Analysis completed'})
    
    @action(detail=False, methods=['get'])
    def by_project(self, request):
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({'error': 'project_id is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        reports = self.get_queryset().filter(project_id=project_id)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)
