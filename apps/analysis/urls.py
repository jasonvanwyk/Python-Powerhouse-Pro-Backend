from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analysis'

router = DefaultRouter()
router.register(r'reports', views.AnalysisReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]