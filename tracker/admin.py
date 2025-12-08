from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Lecturer, Course, Assignment, Submission


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'nrp', 'name', 'email')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('lecturer_id', 'lecturer_name', 'lecturer_email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_code', 'course_name', 'semester', 'lecturer')
    list_filter = ('semester', 'lecturer')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'title', 'course', 'due_date', 'max_score')
    list_filter = ('course',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'student', 'assignment', 'submitted_at', 'score', 'status')
    list_filter = ('assignment', 'student')
