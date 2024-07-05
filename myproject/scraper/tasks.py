from celery import shared_task
from .parser import fetch_resume_data

@shared_task
def fetch_resumes_task(query, min_salary, skills):
    all_resumes = fetch_resume_data(query=query, min_salary=min_salary, skills=skills)
    return all_resumes
