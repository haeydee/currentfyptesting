from django import forms
from .models import Milestone, Submission, Comment, SupervisorRequest
from lecturer.models import LecturerProfile

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['title', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title','file']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
        
class SupervisorRequestForm(forms.ModelForm):
    class Meta:
        model = SupervisorRequest
        fields = ['lecturer', 'fyp_title']
        
        def __init__(self, *args, **kwargs):
            super(SupervisorRequestForm, self).__init__(*args, **kwargs)
            self.fields['lecturer'].queryset = LecturerProfile.objects.all()
            self.fields['lecturer'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} - {obj.expertise}"