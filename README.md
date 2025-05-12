📚 Student Activity Report Generator (Django + Celery)
This project provides a RESTful API for generating and retrieving student activity reports (HTML & PDF) based on event logs. It uses Django, Celery, and PostgreSQL to asynchronously process input data and store reports.

🚀 Features
✅ Accepts a list of student event records

✅ Asynchronously generates HTML and PDF reports using Celery

✅ Supports task status polling with report retrieval

✅ Stores HTML in PostgreSQL and PDFs in the file system

✅ Clean, REST-compliant API design

📦 Tech Stack
Backend: Django, Django REST Framework

Asynchronous Task Queue: Celery with Redis

Database: PostgreSQL

PDF Generation: ReportLab

📁 Project Structure
bash
Copy
Edit
feedback_project/
├── assignment/          # Django app with API logic
├── config/              # Django project config
├── manage.py
├── docker-compose.yml
├── Dockerfile
└── README.md
🛠️ Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/student-report-generator.git
cd student-report-generator
2. Build & Start Services
bash
Copy
Edit
docker-compose up --build
This will start:

Django API at http://localhost:8000

Redis for Celery

PostgreSQL database

Celery worker

🧪 API Usage
📥 Generate HTML Reports
POST /assignment/html

Input: JSON list of student records

Output: Task IDs for tracking

Example:

json
Copy
Edit
[
  {
    "namespace": "ns_example",
    "student_id": "stu_001",
    "student_name": "Alice",
    "score": 90,
    "remarks": "Good work",
    "events": [
      {
        "type": "saved_code",
        "created_time": "2025-05-12T10:15:00Z",
        "unit": 2
      }
    ]
  }
]
📄 Retrieve HTML Report
GET /assignment/html/<task_id>

Returns status and the report HTML (if completed).

📥 Generate PDF Reports
POST /assignment/pdf
Same structure as HTML endpoint.

📄 Download PDF Report
GET /assignment/pdf/<task_id>

Returns PDF file if task is completed.

✅ Future Improvements
 Add authentication

 Add frontend viewer for reports

 Add filtering/search for past reports

 Improve Celery monitoring/logging