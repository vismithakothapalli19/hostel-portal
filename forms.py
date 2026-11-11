from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'first_name', 'last_name', 'email', 'mobile_number', 'room']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS101'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +919876543210'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        selected_room = cleaned_data.get('room')

        if selected_room:
            allocated_count = Student.objects.filter(room=selected_room)
            if self.instance.pk:
                allocated_count = allocated_count.exclude(pk=self.instance.pk)

            if allocated_count.count() >= selected_room.capacity:
                raise forms.ValidationError(
                    f"Room {selected_room.room_number} is full! Maximum capacity is {selected_room.capacity}."
                )

        return cleaned_data

class MobileLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Mobile Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username or Mobile Number'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )