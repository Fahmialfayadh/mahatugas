from django import forms
from .models import Assignment, Lecturer, Submission, Course, Student


from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'max_score']


class SubmissionForm(forms.ModelForm):
    submitted_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    class Meta:
        model = Submission
        fields = ['assignment', 'student', 'submitted_at', 'file_path', 'score', 'remark']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dropdown student pakai nama
        self.fields['student'].queryset = Student.objects.all()
        self.fields['student'].label_from_instance = lambda obj: f"{obj.nrp} - {obj.name}"
        
        
from django import forms
from .models import Lecturer

class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ["lecturer_name", "lecturer_email"]

from .models import Student
from django import forms    

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nrp', 'name', 'email', 'photo_file']
