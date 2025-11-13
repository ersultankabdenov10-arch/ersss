from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Employee, Car

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Қолданушының аты'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Құпия сөз'
        })

    error_messages = {
        "invalid_login": (
            "Дұрыс пайдаланушы аты мен құпия сөзді енгізіңіз. "
            "Екі өріс те регистрге сезімтал."
        ),
        "inactive": ("Бұл аккаунт өшірілген."),
    }

class EmployeeRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False, label='Аватар')
    phone = forms.CharField(
        max_length=20,
        required=True,
        error_messages={'required': 'Телефон нөмірі міндетті.'}
    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Бұл өріс міндетті.', 'invalid': 'Жарамды электрондық поштаны енгізіңіз.'}
    )
    role = forms.ChoiceField(
        choices=Employee.ROLE_CHOICES,
        error_messages={'required': 'Рөлді таңдаңыз.'}
    )
    contact_info = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Бұл өріс міндетті.',
                'unique': 'Мұндай пайдаланушы бұрыннан бар.',
            },
            'password1': {'required': 'Құпия сөзді енгізіңіз.'},
            'password2': {'required': 'Құпия сөзді растаңыз.'},
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        placeholders = {
            'username': 'Пайдаланушының аты',
            'phone': 'Телефон нөмірі',
            'email': 'Электрондық пошта',
            'password1': 'Құпия сөз',
            'password2': 'Құпия сөзді растау',
            'role': 'Жүйедегі рөлі',
            'contact_info': 'Байланыс ақпараты (міндетті емес)',
        }

        for field_name, field in self.fields.items():
            field.label = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Employee.objects.create(
            user=user,
            role=self.cleaned_data['role'],
            phone=self.cleaned_data['phone'],
            contact_info=self.cleaned_data['contact_info'],
            avatar=self.cleaned_data.get('avatar')
        )
        return user

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'car_type', 'price_per_day', 'image', 'location', 'coordinates']
        labels = {
            'image': 'Суреті',  # Только для image показываем метку
        }
        widgets = {
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Бренд (мысалы: Toyota)'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Модель (мысалы: Camry)'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Шыққан жылы (мысалы: 2020)'
            }),
            'car_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автокөліктің типі (мысалы: Седан)'
            }),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Күніне бағасы (мысалы: 15000)'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автокөліктің мекенжайы'
            }),
            'coordinates': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем метки со всех полей, кроме image
        for field_name in self.fields:
            if field_name != 'image':
                self.fields[field_name].label = ''