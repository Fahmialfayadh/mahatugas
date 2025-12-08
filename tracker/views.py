from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Student, Lecturer, Course, Assignment, Submission
from .forms import (
    StudentForm, LecturerForm,
    AssignmentForm, SubmissionForm
)
from django.db.models import F, Avg, Count

# =======================================
# DASHBOARD
# =======================================
def dashboard(request):
    now = timezone.now()
    assignments = Assignment.objects.select_related('course').order_by('due_date')

    data = []
    for a in assignments:
        submitted_count = a.submissions.count()
        if submitted_count == 0 and a.due_date < now:
            status = "Missing"
        elif submitted_count == 0 and a.due_date >= now:
            status = "No Submission Yet"
        else:
            status = "Has Submissions"

        data.append({
            "assignment": a,
            "status": status,
            "submitted_count": submitted_count,
        })

    context = {
        "assignment_status_list": data,
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_assignments": Assignment.objects.count(),
        "total_submissions": Submission.objects.count(),
    }
    return render(request, "tracker/dashboard.html", context)


# =======================================
# STUDENTS CRUD
# =======================================
def students_list(request):
    students = Student.objects.order_by("nrp")
    return render(request, "tracker/students_list.html", {
        "students": students
    })


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("students_list")
    else:
        # Cari NRP terakhir
        last_student = Student.objects.order_by("-nrp").first()
        if last_student and last_student.nrp.isdigit():
            next_nrp_int = int(last_student.nrp) + 1
        else:
            next_nrp_int = 1

        next_nrp = f"{next_nrp_int:03d}"  # 001, 002, 003, ...

        # >>> DI SINI AUTO ISI EMAIL & PHOTO FILE <<<
        initial = {
            "nrp": next_nrp,
            "email": f"{next_nrp}@student.univ.ac.id",
            "photo_file": f"{next_nrp}.jpg",
        }

        form = StudentForm(initial=initial)

    return render(request, "tracker/student_form.html", {
        "form": form,
        "is_edit": False,
        "edit_mode": request.session.get("edit_mode", False),
    })


def student_edit(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("students_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "tracker/student_form.html", {
        "form": form,
        "is_edit": True
    })


def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("students_list")

    return render(request, "tracker/student_delete_confirm.html", {
        "student": student
    })


# =======================================
# LECTURER CRUD
# =======================================
def lecturer_list(request):
    lecturers = Lecturer.objects.all()
    return render(request, "tracker/lecturer_list.html", {
        "lecturers": lecturers,
        "edit_mode": request.session.get("edit_mode", False),
    })

def lecturer_create(request):
    if request.method == "POST":
        form = LecturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lecturer_list")
    else:
        form = LecturerForm()

    return render(request, "tracker/lecturer_form.html", {
        "form": form,
        "is_edit": False,
        "edit_mode": request.session.get("edit_mode", False),   # ← WAJIB
    })
    
def lecturer_edit(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)

    if request.method == "POST":
        form = LecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            return redirect("lecturer_list")
    else:
        form = LecturerForm(instance=lecturer)

    return render(request, "tracker/lecturer_form.html", {
        "form": form,
        "is_edit": True,
        "edit_mode": request.session.get("edit_mode", False),   # ← WAJIB
    })


def lecturer_delete(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
    
    if request.method == "POST":
        lecturer.delete()
        return redirect("lecturer_list")

    return render(request, "tracker/lecturer_delete_confirm.html", {
        "lecturer": lecturer,
        "edit_mode": request.session.get("edit_mode", False),
    })


# =======================================
# COURSES CRUD
# =======================================
def courses_list(request):
    courses = Course.objects.select_related("lecturer").order_by("course_code")
    return render(request, "tracker/courses_list.html", {
        "courses": courses
    })


def course_create(request):
    if request.method == "POST":
        Course.objects.create(
            course_code=request.POST.get("course_code"),
            course_name=request.POST.get("course_name"),
            semester=request.POST.get("semester"),
            lecturer_id=request.POST.get("lecturer")
        )
        return redirect("courses_list")

    lecturers = Lecturer.objects.all()
    return render(request, "tracker/course_form.html", {
        "lecturers": lecturers,
        "is_edit": False
    })


def course_edit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        course.course_code = request.POST.get("course_code")
        course.course_name = request.POST.get("course_name")
        course.semester = request.POST.get("semester")
        course.lecturer_id = request.POST.get("lecturer")
        course.save()
        return redirect("courses_list")

    lecturers = Lecturer.objects.all()
    return render(request, "tracker/course_form.html", {
        "course": course,
        "lecturers": lecturers,
        "is_edit": True
    })


def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        course.delete()
        return redirect("courses_list")

    return render(request, "tracker/course_delete_confirm.html", {
        "course": course
    })


# =======================================
# COURSE DETAIL (ASSIGNMENTS LIST)
# =======================================
def course_detail(request, course_id):
    course = get_object_or_404(Course.objects.select_related("lecturer"), pk=course_id)
    assignments = course.assignments.order_by("due_date")

    return render(request, "tracker/course_detail.html", {
        "course": course,
        "assignments": assignments,
        "edit_mode": request.session.get("edit_mode", False),   # ← WAJIB
    })


# =======================================
# ASSIGNMENT CRUD
# =======================================
def assignment_create(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            return redirect("course_detail", course_id=assignment.course.course_id)
    else:
        form = AssignmentForm()

    return render(request, "tracker/assignment_form.html", {
        "form": form,
        "is_edit": False
    })


def assignment_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect("course_detail", course_id=assignment.course.course_id)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, "tracker/assignment_form.html", {
        "form": form,
        "is_edit": True
    })


def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    course_id = assignment.course.course_id

    if request.method == "POST":
        assignment.delete()
        return redirect("course_detail", course_id=course_id)

    return render(request, "tracker/assignment_delete_confirm.html", {
        "assignment": assignment
    })


# =======================================
# SUBMISSIONS CRUD
# =======================================
def submissions_list(request):
    submissions = Submission.objects.select_related(
        "student", "assignment", "assignment__course"
    ).order_by("-submitted_at")

    return render(request, "tracker/submissions_list.html", {
        "submissions": submissions
    })


def submission_create(request):
    assignment_id = request.GET.get("assignment")

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("submissions_list")
    else:
        form = SubmissionForm(initial={"assignment": assignment_id})

    return render(request, "tracker/submission_form.html", {
        "form": form,
        "is_edit": False,
        "edit_mode": request.session.get("edit_mode", False),
    })



def submission_edit(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return redirect("submissions_list")
    else:
        form = SubmissionForm(instance=submission)

    return render(request, "tracker/submission_form.html", {
        "form": form,
        "is_edit": True
    })


def submission_delete(request, submission_id):
    sub = get_object_or_404(Submission, pk=submission_id)

    if request.method == "POST":
        sub.delete()
        return redirect("submissions_list")

    return render(request, "tracker/submission_delete_confirm.html", {
        "submission": sub
    })


def transcript_view(request):
    submissions = Submission.objects.select_related("student", "assignment__course")
    return render(request, "tracker/transcript.html", {
        "submissions": submissions,
        "courses": Course.objects.all(),
        "all_students": Student.objects.all(),
        "active_course": None,
        "active_student": None,
    })

def transcript_by_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submissions = Submission.objects.filter(assignment__course_id=course_id).select_related("student", "assignment__course")

    return render(request, "tracker/transcript.html", {
        "submissions": submissions,
        "courses": Course.objects.all(),
        "all_students": Student.objects.all(),
        "active_course": course,
        "active_student": None,
    })


def transcript_by_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    submissions = Submission.objects.filter(student_id=student_id).select_related("student", "assignment__course")

    return render(request, "tracker/transcript.html", {
        "submissions": submissions,
        "courses": Course.objects.all(),
        "all_students": Student.objects.all(),
        "active_course": None,
        "active_student": student,
    })

def report_menu(request):
    return render(request, "tracker/reports/report_menu.html")

def report_late_submissions(request):
    submissions = Submission.objects.select_related(
        "student", "assignment__course"
    ).filter(submitted_at__gt=F("assignment__due_date"))

    return render(request, "tracker/reports/late_submissions.html", {
        "submissions": submissions
    })


def report_missing_submissions(request):
    now = timezone.now()
    assignments = Assignment.objects.filter(due_date__lt=now)

    missing = []
    for a in assignments:
        if a.submissions.count() == 0:
            missing.append(a)

    return render(request, "tracker/reports/missing_submissions.html", {"assignments": missing})

from django.db.models import Avg

def report_score_average(request):
    avg_score = Submission.objects.aggregate(Avg("score"))
    return render(request, "tracker/reports/score_average.html", {"avg": avg_score})

def report_score_per_course(request):
    data = Course.objects.annotate(avg_score=Avg("assignments__submissions__score"))
    return render(request, "tracker/reports/score_per_course.html", {"data": data})

def report_no_submission(request):
    assignments = Assignment.objects.annotate(
        total=Count("submissions")
    ).filter(total=0)

    return render(request, "tracker/reports/no_submission.html", {"assignments": assignments})

    return render(request, "tracker/reports/no_submission.html", {"assignments": assignments})

def report_top_students(request):
    top = Submission.objects.order_by("-score")[:10]
    return render(request, "tracker/reports/top_students.html", {"submissions": top})

def report_low_students(request):
    low = Submission.objects.order_by("score")[:10]
    return render(request, "tracker/reports/low_students.html", {"submissions": low})

from django.db.models import Count

def report_submission_count(request):
    data = Student.objects.annotate(total=Count("submissions")).order_by("-total")
    return render(request, "tracker/reports/submission_count.html", {"data": data})

def report_assignment_popularity(request):
    data = Assignment.objects.annotate(total=Count("submissions")).order_by("-total")
    return render(request, "tracker/reports/assignment_popularity.html", {"data": data})
def report_sort_submissions(request):
    sort = request.GET.get("by", "asc")
    if sort == "desc":
        submissions = Submission.objects.order_by("-score")
    else:
        submissions = Submission.objects.order_by("score")

    return render(request, "tracker/reports/sort_submissions.html", {
        "submissions": submissions,
        "sort": sort
    })



from django.db import connection

QUERIES = {
    1: "SELECT AVG(score) AS avg_score FROM tracker_submission;",
    2: """
        SELECT c.course_name, AVG(s.score) AS avg_score
        FROM tracker_submission s
        JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
        JOIN tracker_course c ON a.course_id = c.course_id
        GROUP BY c.course_name;
    """,
    3: """
        SELECT st.name, COUNT(s.submission_id) AS total_submit
        FROM tracker_student st
        LEFT JOIN tracker_submission s ON st.student_id = s.student_id
        GROUP BY st.name;
    """,
    4: """
        SELECT c.course_name, COUNT(a.assignment_id) AS total_assignments
        FROM tracker_course c
        LEFT JOIN tracker_assignment a ON c.course_id = a.course_id
        GROUP BY c.course_name;
    """,
    5: """
        SELECT a.title, COUNT(s.submission_id) AS submission_count
        FROM tracker_assignment a
        LEFT JOIN tracker_submission s ON a.assignment_id = s.assignment_id
        GROUP BY a.title
        ORDER BY submission_count DESC
        LIMIT 1;
    """,
    6: """
        SELECT name, score
        FROM tracker_student
        JOIN tracker_submission USING(student_id)
        WHERE score = (SELECT MAX(score) FROM tracker_submission);
    """,
    7: """
        SELECT title
        FROM tracker_assignment
        WHERE assignment_id NOT IN (
            SELECT assignment_id FROM tracker_submission
        );
    """,
    8: """
        SELECT lecturer_name
        FROM tracker_lecturer
        WHERE lecturer_id IN (
            SELECT lecturer_id
            FROM tracker_course
            GROUP BY lecturer_id
            HAVING COUNT(*) > 1
        );
    """,
    9: """
        SELECT name
        FROM tracker_student
        WHERE student_id NOT IN (
            SELECT student_id 
            FROM tracker_submission
            JOIN tracker_assignment USING(assignment_id)
            WHERE course_id = 1
        );
    """,
    10: """
        SELECT st.name, AVG(s.score) AS avg_student
        FROM tracker_student st
        JOIN tracker_submission s ON st.student_id = s.student_id
        GROUP BY st.student_id
        HAVING AVG(s.score) > (
            SELECT AVG(score) FROM tracker_submission
        );
    """,
    11: """
        SELECT st.name, a.title, s.submitted_at, a.due_date
        FROM tracker_submission s
        JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
        JOIN tracker_student st ON s.student_id = st.student_id
        WHERE s.submitted_at > a.due_date;
    """,
    12: """
        SELECT st.name, a.title, s.submitted_at
        FROM tracker_submission s
        JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
        JOIN tracker_student st ON s.student_id = st.student_id
        WHERE s.submitted_at <= a.due_date;
    """,
    13: """
        SELECT c.course_code, c.course_name, l.lecturer_name
        FROM tracker_course c
        JOIN tracker_lecturer l ON c.lecturer_id = l.lecturer_id;
    """,
    14: """
        SELECT st.name AS student, c.course_name, a.title, s.score
        FROM tracker_submission s
        JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
        JOIN tracker_course c ON a.course_id = c.course_id
        JOIN tracker_student st ON s.student_id = st.student_id;
    """,
    15: """
        SELECT title, due_date
        FROM tracker_assignment
        WHERE due_date < CURRENT_TIMESTAMP;
    """,
}


def queries_menu(request):
    return render(request, "tracker/queries/menu.html", {"queries": QUERIES})


def run_query(request, q_id):
    sql = QUERIES.get(q_id)
    if not sql:
        return render(request, "tracker/queries/result.html", {
            "error": "Query not found",
        })

    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = cursor.fetchall()

    return render(request, "tracker/queries/result.html", {
        "query": sql,
        "columns": columns,
        "rows": rows,
    })
    
def assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    
    # Semua student
    students = Student.objects.all()

    # Semua submissions untuk assignment ini
    submissions = Submission.objects.filter(assignment_id=assignment_id)

    submitted_ids = submissions.values_list("student_id", flat=True)

    # Cari student yang belum submit
    missing_students = students.exclude(student_id__in=submitted_ids)

    return render(request, "tracker/assignment_submissions.html", {
        "assignment": assignment,
        "submissions": submissions,
        "missing_students": missing_students,
        "edit_mode": request.session.get("edit_mode", False),
    })


def overview_view(request):
    description = "Database ini dirancang untuk mengelola data mahasiswa, dosen, mata kuliah, tugas, dan submission dengan relasi terstruktur dan otomatis."

    context = {
        "description": description,
        "student_count": Student.objects.count(),
        "lecturer_count": Lecturer.objects.count(),
        "course_count": Course.objects.count(),
        "assignment_count": Assignment.objects.count(),
        "submission_count": Submission.objects.count(),
    }

    return render(request, "tracker/overview.html", context)

# =========================================================================
#                           EDIT MODE TOGGLE
# =========================================================================
def toggle_edit_mode(request):
    current = request.session.get("edit_mode", False)
    request.session["edit_mode"] = not current
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))
