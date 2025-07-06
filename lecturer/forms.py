from django import forms
from .models import LecturerProfile, ClassMaterial

class LecturerClassForm(forms.ModelForm):
    class Meta:
        model = LecturerProfile
        fields = ['assigned_kumpulan']
        widgets = {
            'assigned_kumpulan': forms.CheckboxSelectMultiple
        }
        
class ClassMaterialForm(forms.ModelForm):
    class Meta:
        model = ClassMaterial
        fields = ['title', 'description', 'file']