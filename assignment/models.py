from django.db import models

class HTMLReport(models.Model):
    student_id = models.CharField(max_length=64)
    task_id = models.CharField(max_length=64, unique=True)
    content = models.TextField()

class PDFReport(models.Model):
    student_id = models.CharField(max_length=64)
    task_id = models.CharField(max_length=64, unique=True)
    pdf_file = models.FileField(upload_to='pdf_reports/')
