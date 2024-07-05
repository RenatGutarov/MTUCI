from bs4 import BeautifulSoup
import requests
import re
from fake_useragent import UserAgent
from .models import Resume  # Импортируем модель Resume из файла models.py вашего приложения

def fetch_resume_data(query='python', min_salary=None, skills=None, area=1, page_size=20):
    ua = UserAgent()
    page = 0
    all_resumes = []

    while True:
        url = f"https://hh.ru/search/resume?area={area}&exp_period=all_time&logic=normal&" \
              f"no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&" \
              f"search_period=0&text={query}&items_on_page={page_size}&page={page}"
        print(f"Fetching data from URL: {url}")

        response = requests.get(url, headers={'User-Agent': ua.chrome})
        print(f"Response status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'lxml')
        urls = soup.find_all('a', {'data-qa': "serp-item__title", 'class': "bloko-link"})

        if not urls:
            break

        for url in urls:
            resume_info = {}
            href = 'https://hh.ru/' + url.attrs['href']
            print(f"Fetching resume details from URL: {href}")

            response = requests.get(href, headers={'User-Agent': ua.chrome})
            print(f"Response status code for resume details: {response.status_code}")

            soup = BeautifulSoup(response.text, 'lxml')

            salary_obj = soup.find('span', {'class': 'resume-block__salary'})
            if salary_obj:
                salary_text = salary_obj.text.strip()
                salary_digits = re.findall(r'\d+', salary_text)
                salary = int(''.join(salary_digits))
            else:
                salary = None

            if min_salary and salary is not None and salary < min_salary:
                print(f"Skipping resume '{href}' due to salary requirement.")
                continue

            title_obj = soup.find('span', {'class': 'resume-block__title-text'})
            job_title = title_obj.text.strip() if title_obj else 'Не указано'

            skills_obj = soup.find('div', {'class': 'bloko-tag-list'})
            if skills_obj:
                skills_list = [
                    tag.text.strip()
                    for tag in skills_obj.find_all('span', {'class': 'bloko-tag__section_text'})
                ]
                skills_text = ', '.join(skills_list)
            else:
                skills_text = 'Не указано'

            print(f"Job title: {job_title}")
            print(f"Salary: {salary}")
            print(f"Skills: {skills_text}")

            # Проверка наличия всех указанных навыков
            if skills:
                required_skills = set(skills.split(', '))
                resume_skills = set(skills_list)
                if not required_skills.issubset(resume_skills):
                    print(f"Skipping resume '{href}' due to lack of required skills.")
                    continue

            # Сохранение резюме в базу данных
            try:
                if salary is None and min_salary:
                    print(f"Skipping resume '{href}' due to missing salary.")
                    continue

                resume = Resume(
                    title=job_title,
                    salary=salary if salary is not None else 0,  # Установка значения по умолчанию, если salary None
                    skills=skills_text
                )
                resume.save()
                print("Resume saved to database.")
                all_resumes.append(resume)
            except Exception as e:
                print(f"Error saving resume to database: {e}")

        page += 1

    return all_resumes


























