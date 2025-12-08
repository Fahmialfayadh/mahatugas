from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.students_list, name='students_list'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),

    # Courses
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Reports
    path('reports/', views.report_menu, name='report_menu'),
    path('reports/late-submissions/', views.report_late_submissions, name='report_late_submissions'),
    path('reports/missing-submissions/', views.report_missing_submissions, name='report_missing_submissions'),
    path('reports/score-average/', views.report_score_average, name='report_score_average'),
    path('reports/score-per-course/', views.report_score_per_course, name='report_score_per_course'),
    path('reports/no-submission/', views.report_no_submission, name='report_no_submission'),
    path('reports/top-students/', views.report_top_students, name='report_top_students'),
    path('reports/low-students/', views.report_low_students, name='report_low_students'),
    path('reports/submission-count/', views.report_submission_count, name='report_submission_count'),
    path('reports/assignment-popularity/', views.report_assignment_popularity, name='report_assignment_popularity'),
    path('reports/sort-submissions/', views.report_sort_submissions, name='report_sort_submissions'),


    # Assignments
    path('assignments/new/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:assignment_id>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),

    # Submissions
    path('submissions/', views.submissions_list, name='submissions_list'),
    path('submissions/new/', views.submission_create, name='submission_create'),
    path('submissions/<int:submission_id>/edit/', views.submission_edit, name='submission_edit'),
    path('submissions/<int:submission_id>/delete/', views.submission_delete, name='submission_delete'),

    # Transcript
    path('transcript/', views.transcript_view, name='transcript'),
    path('transcript/course/<int:course_id>/', views.transcript_by_course, name='transcript_by_course'),
    path('transcript/student/<int:student_id>/', views.transcript_by_student, name='transcript_by_student'),
    
    # Lecturers
    path('lecturers/', views.lecturer_list, name='lecturer_list'),
    path('lecturers/new/', views.lecturer_create, name='lecturer_create'),
    path('lecturers/<int:lecturer_id>/edit/', views.lecturer_edit, name='lecturer_edit'),
    path('lecturers/<int:lecturer_id>/delete/', views.lecturer_delete, name='lecturer_delete'),

    # Queries Demo
    path("queries/", views.queries_menu, name="queries_menu"),
    path("queries/<int:q_id>/", views.run_query, name="run_query"),
    
    
    path('overview/', views.overview_view, name='overview'),
    
    path("assignments/<int:assignment_id>/submissions/", views.assignment_submissions, name="assignment_submissions"),

    
    # Edit mode toggle
    path('toggle-edit/', views.toggle_edit_mode, name='toggle_edit'),
    
]
