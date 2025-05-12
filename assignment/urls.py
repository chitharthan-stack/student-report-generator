from django.urls import path
from .views import *

urlpatterns = [
    path('html', HTMLReportView.as_view()),
    path('html/<str:task_id>', HTMLReportStatusView.as_view()),
    path('pdf', PDFReportView.as_view()),
    path('pdf/<str:task_id>', PDFReportStatusView.as_view()),
]
