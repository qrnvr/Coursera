# Coursera

Django Online Course app with an exam (assessment) feature: lessons, questions with choices,
learner submissions, and a result page.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations onlinecourse
python3 manage.py migrate
python3 manage.py seed_demo        # creates a demo course with an exam
python3 manage.py createsuperuser
python3 manage.py runserver
```

- Site: http://127.0.0.1:8000/ (log in, open the course, enroll, take the exam)
- Admin: http://127.0.0.1:8000/admin/
- Tests: `python3 manage.py test`

## Where the exam code lives

- `onlinecourse/models.py` - `Question`, `Choice`, `Submission`
- `onlinecourse/admin.py` - `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, `LessonAdmin`
- `onlinecourse/views.py` - `submit`, `show_exam_result`
- `onlinecourse/urls.py` - routes for `submit` and `show_exam_result`
- `onlinecourse/templates/onlinecourse/` - course details and exam result templates
