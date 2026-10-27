from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='onlinecourse/login.html'),
        name='login',
    ),
    path('logout/', views.logout_request, name='logout'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    # Submit the exam answers
    path('<int:course_id>/submit/', views.submit, name='submit'),
    # Show the exam result
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result',
    ),
]
