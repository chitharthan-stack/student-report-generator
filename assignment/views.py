# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ReportRequestSerializer
# from .tasks import generate_html_report, generate_pdf_report
# from .models import HTMLReport, PDFReport
# from celery.result import AsyncResult
# from django.http import FileResponse, Http404


# class HTMLReportView(APIView):
#     def post(self, request):
#         data = request.data

#         # Handle stringified JSON (in case client sends it that way)
#         if isinstance(data, str):
#             try:
#                 data = json.loads(data)
#             except json.JSONDecodeError:
#                 return Response({"error": "Invalid JSON format."}, status=400)

#         if not isinstance(data, list):
#             return Response({"error": "Expected a list of student records."}, status=400)

#         serializer = ReportRequestSerializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)

#         task_ids = []
#         for student_data in serializer.validated_data:
#             task = generate_html_report.delay(student_data)
#             task_ids.append(task.id)

#         return Response({"task_ids": task_ids}, status=status.HTTP_202_ACCEPTED)


# class HTMLReportStatusView(APIView):
#     def get(self, request, task_id):
#         result = AsyncResult(task_id)
#         if result.successful():
#             try:
#                 report = HTMLReport.objects.get(task_id=task_id)
#                 return Response({"status": "completed", "html": report.content})
#             except HTMLReport.DoesNotExist:
#                 raise Http404()
#         return Response({"status": result.status})


# class PDFReportView(APIView):
#     def post(self, request):
#         data = request.data

#         # Handle stringified JSON
#         if isinstance(data, str):
#             try:
#                 data = json.loads(data)
#             except json.JSONDecodeError:
#                 return Response({"error": "Invalid JSON format."}, status=400)

#         if not isinstance(data, list):
#             return Response({"error": "Expected a list of student records."}, status=400)

#         serializer = ReportRequestSerializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)

#         task_ids = []
#         for student_data in serializer.validated_data:
#             task = generate_pdf_report.delay(student_data)
#             task_ids.append(task.id)

#         return Response({"task_ids": task_ids}, status=status.HTTP_202_ACCEPTED)


# class PDFReportStatusView(APIView):
#     def get(self, request, task_id):
#         result = AsyncResult(task_id)
#         if result.successful():
#             try:
#                 report = PDFReport.objects.get(task_id=task_id)
#                 return FileResponse(report.pdf_file.open(), as_attachment=True, filename="report.pdf")
#             except PDFReport.DoesNotExist:
#                 raise Http404()
#         return Response({"status": result.status})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReportRequestSerializer
from .tasks import generate_html_report, generate_pdf_report
from .models import HTMLReport, PDFReport
from celery.result import AsyncResult
from django.http import FileResponse, Http404


class HTMLReportView(APIView):
    def post(self, request):
        print("✅ Received request in HTMLReportView")
        print("📦 request.data:", request.data)
        serializer = ReportRequestSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        task_ids = []
        for student_data in serializer.validated_data:
            task = generate_html_report.delay(student_data)
            task_ids.append(task.id)

        return Response({"task_ids": task_ids}, status=status.HTTP_202_ACCEPTED)


class HTMLReportStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.successful():
            try:
                report = HTMLReport.objects.get(task_id=task_id)
                return Response({"status": "completed", "html": report.content})
            except HTMLReport.DoesNotExist:
                raise Http404()
        return Response({"status": result.status})


class PDFReportView(APIView):
    def post(self, request):
        serializer = ReportRequestSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        task_ids = []
        for student_data in serializer.validated_data:
            task = generate_pdf_report.delay(student_data)
            task_ids.append(task.id)

        return Response({"task_ids": task_ids}, status=status.HTTP_202_ACCEPTED)


class PDFReportStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.successful():
            try:
                report = PDFReport.objects.get(task_id=task_id)
                return FileResponse(report.pdf_file.open(), as_attachment=True, filename="report.pdf")
            except PDFReport.DoesNotExist:
                raise Http404()
        return Response({"status": result.status})
