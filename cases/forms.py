from django import forms
from .models import Case, Document

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'category', 'status', 'phone_number']
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']  

class CaseSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
    category = forms.ChoiceField(label='Category', choices=[('', 'All')] + Case.CATEGORY_CHOICES, required=False)
    status = forms.ChoiceField(label='Status', choices=[('', 'All')] + Case.STATUS_CHOICES, required=False)
