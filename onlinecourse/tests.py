from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Enrollment, Submission


class ExamFlowTests(TestCase):
    def setUp(self):
        call_command('seed_demo', verbosity=0)
        self.course = Course.objects.get(name='Introduction to Python')
        self.user = User.objects.create_user('student', password='pass12345')
        self.client.login(username='student', password='pass12345')
        self.client.post(reverse('onlinecourse:enroll', args=(self.course.id,)))

    def answers(self, correct):
        data = {}
        for choice in Choice.objects.filter(question__lesson__course=self.course):
            if choice.is_correct == correct:
                data[f'choice_{choice.id}'] = choice.id
        return data

    def submit(self, correct):
        return self.client.post(
            reverse('onlinecourse:submit', args=(self.course.id,)),
            self.answers(correct),
            follow=True,
        )

    def test_enroll_creates_enrollment(self):
        self.assertTrue(
            Enrollment.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_course_detail_shows_lessons_and_exam(self):
        response = self.client.get(
            reverse('onlinecourse:course_details', args=(self.course.id,))
        )
        self.assertContains(response, 'Introduction to Python')
        self.assertContains(response, 'Variables and types')
        self.assertContains(response, 'Which keyword defines a function?')

    def test_passing_attempt_shows_congratulations(self):
        response = self.submit(correct=True)
        self.assertContains(response, 'Congratulations')
        self.assertContains(response, '100 / 100')
        self.assertEqual(Submission.objects.count(), 1)

    def test_failing_attempt_shows_failed(self):
        response = self.submit(correct=False)
        self.assertContains(response, 'Failed')
        self.assertNotContains(response, 'Congratulations')

    def test_anonymous_submit_redirects_to_login(self):
        self.client.logout()
        response = self.client.post(
            reverse('onlinecourse:submit', args=(self.course.id,))
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class AdminTests(TestCase):
    def test_admin_index_lists_sections(self):
        User.objects.create_superuser('admin', 'admin@example.com', 'pass12345')
        self.client.login(username='admin', password='pass12345')
        response = self.client.get('/admin/')
        self.assertContains(response, 'Authentication and Authorization')
        self.assertContains(response, 'OnlineCourse')
