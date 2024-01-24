from django import forms
from .models import Catogry
class CatogryForm(forms.ModelForm):
    class Meta:
        model = Catogry
        fields = ['name','descripe']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to individual fields
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripe'].widget.attrs.update({'class': 'form-control'})