from celery import shared_task
from .models import HTMLReport, PDFReport
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

@shared_task(bind=True)
def generate_html_report(self, payload):
    student_id = payload["student_id"]
    student_name = payload["student_name"]
    score = payload["score"]
    remarks = payload["remarks"]
    events = sorted(payload["events"], key=lambda x: x["unit"])
    
    unit_to_q = {}
    q_number = 1
    result = []

    for e in events:
        unit = e["unit"]
        if unit not in unit_to_q:
            unit_to_q[unit] = f"Q{q_number}"
            q_number += 1
        result.append(unit_to_q[unit])

    html = f"""
    <h2>Student ID: {student_id}</h2>
    <p>Name: {student_name}</p>
    <p>Score: {score}</p>
    <p>Remarks: {remarks}</p>
    <p>Event Order: {' -> '.join(result)}</p>
    """
    
    HTMLReport.objects.create(
        student_id=student_id,
        task_id=self.request.id,
        content=html
    )
    return self.request.id


@shared_task(bind=True)
def generate_pdf_report(self, payload):
    student_id = payload["student_id"]
    student_name = payload["student_name"]
    score = payload["score"]
    remarks = payload["remarks"]
    events = sorted(payload["events"], key=lambda x: x["unit"])
    
    unit_to_q = {}
    q_number = 1
    result = []

    for e in events:
        unit = e["unit"]
        if unit not in unit_to_q:
            unit_to_q[unit] = f"Q{q_number}"
            q_number += 1
        result.append(unit_to_q[unit])

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Positioning
    y = 800
    p.drawString(100, y, f"Student ID: {student_id}")
    y -= 20
    p.drawString(100, y, f"Name: {student_name}")
    y -= 20
    p.drawString(100, y, f"Score: {score}")
    y -= 20
    p.drawString(100, y, f"Remarks: {remarks}")
    y -= 40
    p.drawString(100, y, f"Event Order: {' -> '.join(result)}")
    p.showPage()
    p.save()

    file_name = f"{uuid.uuid4()}.pdf"
    report = PDFReport(student_id=student_id, task_id=self.request.id)
    report.pdf_file.save(file_name, ContentFile(buffer.getvalue()))
    report.save()

    return self.request.id
