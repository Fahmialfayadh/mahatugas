from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Student(models.Model):
    def generate_nrp():
        # Ambil student terakhir
        last_student = Student.objects.order_by("-student_id").first()

        if last_student and last_student.nrp.isdigit():
            new_nrp = int(last_student.nrp) + 1
        else:
            new_nrp = 1  # kalau belum ada student

        return f"{new_nrp:03d}"  # format 3 digit, misal 001
    student_id = models.AutoField(primary_key=True)
    nrp = models.CharField(
    max_length=20,
    unique=True,
    default=generate_nrp,
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, blank=True, null=True)
    photo_file = models.CharField(max_length=255, blank=True, null=True)  # path avatar

    def __str__(self):
        return f"{self.nrp} - {self.name}"


class Lecturer(models.Model):
    lecturer_id = models.AutoField(primary_key=True)

    lecturer_name = models.CharField(max_length=200)
    lecturer_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.lecturer_name



class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    semester = models.IntegerField()
    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.title} ({self.course.course_code})"


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    file_path = models.FileField(upload_to='submissions/')
    score = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"

    @property
    def status(self):
        """
        Status logic:
        - SubmittedAt > DueDate   -> "Late"
        - SubmittedAt <= DueDate  -> "On Time"
        (Kalau mau handle Missing, bisa pakai join assignments tanpa submission)
        """
        if self.submitted_at and self.assignment.due_date:
            if self.submitted_at > self.assignment.due_date:
                return "Late"
            else:
                return "On Time"
        return "-"
