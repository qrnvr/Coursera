from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .models import Course, Enrollment, Question, Submission


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-total_enrollment', 'name')[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_enrolled'] = (
            user.is_authenticated
            and Enrollment.objects.filter(user=user, course=self.object).exists()
        )
        return context


def enroll(request, course_id):
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user, course=course
        )
        if created:
            course.total_enrollment += 1
            course.save()
    return HttpResponseRedirect(
        reverse('onlinecourse:course_details', args=(course.id,))
    )


# ---- Assessment feature (final project) ----

def extract_answers(request):
    """Collect the ids of all choices ticked in the exam form."""
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            submitted_answers.append(int(request.POST[key]))
    return submitted_answers


def submit(request, course_id):
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')
    course = get_object_or_404(Course, pk=course_id)
    if request.method != 'POST':
        return HttpResponseRedirect(
            reverse('onlinecourse:course_details', args=(course.id,))
        )
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(extract_answers(request))
    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    if not request.user.is_authenticated:
        return redirect('onlinecourse:login')
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, pk=submission_id, enrollment__user=request.user
    )
    selected_ids = [choice.id for choice in submission.choices.all()]

    questions = Question.objects.filter(lesson__course=course)
    total_score = 0
    score = 0
    for question in questions:
        total_score += question.grade
        if question.is_get_score(selected_ids):
            score += question.grade

    grade = int(score / total_score * 100) if total_score else 0

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'questions': questions,
        'score': score,
        'total_score': total_score,
        'grade': grade,
        'passed': grade >= 80,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
