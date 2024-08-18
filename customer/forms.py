from django import forms

from customer.models import User, Customer



class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email','phone','image','slug','address']

