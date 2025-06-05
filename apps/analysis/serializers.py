from rest_framework import serializers
from .models import AnalysisReport, CodeQualityMetric, SecurityIssue, PerformanceMetric, TestCoverage


class SecurityIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIssue
        fields = '__all__'


class CodeQualityMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeQualityMetric
        fields = '__all__'


class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = '__all__'


class TestCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCoverage
        fields = '__all__'


class AnalysisReportSerializer(serializers.ModelSerializer):
    security_issues = SecurityIssueSerializer(many=True, read_only=True)
    quality_metrics = CodeQualityMetricSerializer(many=True, read_only=True)
    performance_metrics = PerformanceMetricSerializer(many=True, read_only=True)
    test_coverage = TestCoverageSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnalysisReport
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'started_at', 'completed_at')


class AnalysisReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ('project', 'analysis_type')
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)