from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import EmailSenderTo

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','is_superuser','password1','password2']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

        for key ,field in self.fields.items():
            if key != "is_superuser":
                field.widget.attrs['class'] = "form-control"
            
class UserFormUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','is_superuser','email']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for key ,field in self.fields.items():
            field.widget.attrs['class'] = "form-control"

class emailForm(forms.ModelForm):
    class Meta:
        model = EmailSenderTo
        fields = "__all__"