from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from booker.models import Account, Booking


class AccountForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'maxlength': 100,
            'required': True,
        }),
        label='Confirm Password',
    )

    class Meta:
        model = Account
        fields = [
            'first_name',
            'second_name',
            'nickname',
            'email',
            'phone_number',
            'password',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'aria-describedby': 'id_first_name_helptext',
                'maxlength': 30,
                'required': True,
            }),
            'second_name': forms.TextInput(attrs={
                'placeholder': 'Enter your second name',
                'aria-describedby': 'id_second_name_helptext',
                'maxlength': 30,
                'required': True,
            }),
            'nickname': forms.TextInput(attrs={
                'placeholder': 'Enter your nickname',
                'aria-describedby': 'id_nickname_helptext',
                'maxlength': 30,
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter a valid email address...',
                'maxlength': 100,
                'required': True,
            }),
            'phone_number': forms.NumberInput(attrs={
                'placeholder': 'Enter your phone number...',
                'maxlength': 10,
                'required': True,
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter a secure password',
                'maxlength': 100,
                'required': True,
            })
        }
        labels = {
            'first_name': 'First Name',
            'second_name': 'Second Name',
            'nickname': 'Nickname',
            'email': 'Email',
            'phone_number': 'Phone Number',
        }

        help_texts = {
            'nickname': '*Nicknames can contain only letters and digits.',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError('Enter a valid 10-digit phone number')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match')
            if len(password) < 8:
                raise ValidationError('Password must be at least 8 characters long')

        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.password = make_password(self.cleaned_data['password'])  # hash the password, much secure
        if commit:
            account.save()
        return account


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date': 'Select a date for your booking',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # pop the user from kwargs
        super().__init__(*args, **kwargs)