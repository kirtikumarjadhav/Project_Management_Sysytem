from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    # Sample choices for the dropdown fields
    REASON_CHOICES = [
        ('for_business', 'For Business'),
        ('for_personal', 'For Personal'),
        ('other', 'Other'),
    ]
    
    TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
        ('mixed', 'Mixed'),
    ]
    
    DIVISION_CHOICES = [
        ('division_a', 'Division A'),
        ('division_b', 'Division B'),
        ('division_c', 'Division C'),
    ]
    
    CATEGORY_CHOICES = [
        ('category_1', 'Category 1'),
        ('category_2', 'Category 2'),
        ('category_3', 'Category 3'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('dept_1', 'Department 1'),
        ('dept_2', 'Department 2'),
        ('dept_3', 'Department 3'),
    ]
    
    LOCATION_CHOICES = [
        ('location_1', 'Location 1'),
        ('location_2', 'Location 2'),
        ('location_3', 'Location 3'),
    ]
    
    # Status is not included as a field because it has a default value and might not be changeable by the user

    reason = forms.ChoiceField(choices=REASON_CHOICES)
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    division = forms.ChoiceField(choices=DIVISION_CHOICES)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    location = forms.ChoiceField(choices=LOCATION_CHOICES)

    class Meta:
        model = Project
        fields = '__all__'  # Include all fields
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than the start date.")
        return cleaned_data
