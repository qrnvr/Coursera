from datetime import date

from django.core.management.base import BaseCommand

from onlinecourse.models import Choice, Course, Lesson, Question


class Command(BaseCommand):
    help = 'Create a demo course with two lessons and a short exam'

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            name='Introduction to Python',
            defaults={
                'description': 'A short demo course used to try the exam feature.',
                'pub_date': date.today(),
            },
        )
        if not created and Question.objects.filter(lesson__course=course).exists():
            self.stdout.write('Demo course already exists, nothing to do.')
            return

        lesson1 = Lesson.objects.create(
            course=course,
            order=0,
            title='Variables and types',
            content='Python has built-in types such as int, str and list.',
        )
        lesson2 = Lesson.objects.create(
            course=course,
            order=1,
            title='Functions',
            content='Functions are defined with the def keyword.',
        )

        q1 = Question.objects.create(
            lesson=lesson1,
            question_text='Which of these are built-in Python types?',
            grade=40,
        )
        for text, correct in [('int', True), ('str', True), ('list', True), ('char', False)]:
            Choice.objects.create(question=q1, choice_text=text, is_correct=correct)

        q2 = Question.objects.create(
            lesson=lesson1,
            question_text='What does len([1, 2, 3]) return?',
            grade=30,
        )
        for text, correct in [('2', False), ('3', True), ('4', False)]:
            Choice.objects.create(question=q2, choice_text=text, is_correct=correct)

        q3 = Question.objects.create(
            lesson=lesson2,
            question_text='Which keyword defines a function?',
            grade=30,
        )
        for text, correct in [('def', True), ('fn', False), ('function', False), ('define', False)]:
            Choice.objects.create(question=q3, choice_text=text, is_correct=correct)

        self.stdout.write(self.style.SUCCESS('Demo course "Introduction to Python" created.'))
