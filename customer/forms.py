from django import forms

from customer.models import User, Customer



class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email','phone','image','slug','address']
class LoginFrom(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255,required=False)

    class Meta:
        model = User
        fields = ('email', 'email', 'password')

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already exists')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user
