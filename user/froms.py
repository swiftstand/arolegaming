from django import forms
from django.contrib.auth.forms import  UserCreationForm
from user.models import  User
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    fullname=forms.CharField(max_length=90,required=True)
    email=forms.EmailField(required=True,help_text='Required. add an email')
    class Meta:
        model = User
        fields = ('fullname','email','password1','password2')

    def __init__(self, *args, **kwargs):
        """specifying the field styles"""

        super(UserRegistrationForm,self).__init__(*args,**kwargs)
        for field in (self.fields['email'], self.fields['fullname'], self.fields['password1'],self.fields['password2']):
            field.widget.attrs.update({'class':'form-control'})


class UserLoginForm(forms.ModelForm):
    """for logging in users"""

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','password']
        widgets = {
                    'email':forms.TextInput(attrs={'class':'form-control'}),
                    'password':forms.TextInput(attrs={'class':'form-control'})
        }


    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')
            

