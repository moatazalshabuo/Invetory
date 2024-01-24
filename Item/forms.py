from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['service_tag','catogry','modal', 'store','supplier','type_device', 'purchase_date','Warranty_date']

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        # Add any additional customization here, if needed
        # Apply Bootstrap form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name in ['catogry','modal','store']:
                field.widget.attrs['class'] = 'form-control selete2 id_'+field_name
            else:
                field.widget.attrs['class'] = 'form-control id_'+field_name
        self.fields['purchase_date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        self.fields['Warranty_date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
# Remember

class ModalForm(forms.ModelForm):
    class Meta:
        model = ModelDevice
        
        fields = ['name','catogry','min_device']
    def __init__(self, *args, **kwargs):
        super(ModalForm,self).__init__(*args, **kwargs)
        # Add any additional customization here, if needed
        # Apply Bootstrap form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        
        fields = ['name',]
        
        
class FileDeviceForm(forms.ModelForm):
    class Meta:
        model = DeviceFile
        
        fields = ['file',]
        
    def __init__(self,*args, **kwargs):
        super(FileDeviceForm, self).__init__(*args, **kwargs)
        
        self.fields['file'].required = False
        self.fields['file'].widget = forms.FileInput({'class':'form-control'})
        self.fields['file'].label = 'A copy of the invoice'
        
class HistoryDeviceForm(forms.ModelForm):
    class Meta:
        model = HistoryDevice
        fields = ['status','detiles']
        
    
    def __init__(self, *args, **kwargs):
        super(HistoryDeviceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['name']  # Add more fields if needed
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to individual fields
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        
class officeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['name','department']
        
class DeprtDeviceForm(forms.ModelForm):
    class Meta:
        model = DeprtDevice
        fields = ['device','departments','office']


class ModelSparePartForm(forms.ModelForm):
    class Meta:
        model = ModelSparePart
        fields = ['name',]    
        
class SepraPartForms(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['service_tag','model','store','supplier','Warranty_date','purchase_date','descripe']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['purchase_date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        self.fields['Warranty_date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        # Remember
        for key,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        
    