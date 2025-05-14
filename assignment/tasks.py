from celery import shared_task
from .models import HTMLReport, PDFReport
from reportlab.pdfgen import canvas
import io

@shared_task(bind=True)
def generate_html_report(self, payload):
    try:
        student_id = payload["student_id"]
        events = sorted(payload["events"], key=lambda x: x["unit"])

        unit_to_q = {}
        q_number = 1
        result = []

        for event in events:
            unit = event["unit"]
            if unit not in unit_to_q:
                unit_to_q[unit] = f"Q{q_number}"
                q_number += 1
            result.append(unit_to_q[unit])

        html = f"<h2>Student ID: {student_id}</h2><p>Event Order: {' -> '.join(result)}</p>"

        HTMLReport.objects.create(
            student_id=student_id,
            task_id=self.request.id,
            content=html
        )

        return self.request.id
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)


@shared_task(bind=True)
def generate_pdf_report(self, payload):
    try:
        student_id = payload["student_id"]
        events = sorted(payload["events"], key=lambda x: x["unit"])

        unit_to_q = {}
        q_number = 1
        result = []

        for event in events:
            unit = event["unit"]
            if unit not in unit_to_q:
                unit_to_q[unit] = f"Q{q_number}"
                q_number += 1
            result.append(unit_to_q[unit])

        output = io.BytesIO()
        p = canvas.Canvas(output)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Student ID: {student_id}")
        p.drawString(100, 780, f"Event Order: {' -> '.join(result)}")
        p.showPage()
        p.save()
        output.seek(0)

        PDFReport.objects.create(
            student_id=student_id,
            task_id=self.request.id,
            pdf_file=output.read()
        )

        return self.request.id
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
