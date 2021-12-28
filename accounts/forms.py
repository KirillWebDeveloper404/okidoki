from django.forms import ModelForm
from django.forms.widgets import CheckboxInput, DateInput, TextInput, TimeInput

from .models import User

import datetime

class UserRegisterForm(ModelForm):
    
    class Meta:
        model = User 
        fields = ['name', 'phone', 'email', 'date_burn', 'pasport', 'pasport_otdel', 'pasport_code', 'date_pasport', 'registr', 'organisation', 'inn', 'ogrn', 'name_bank', 'bik', 'schet', 'korp_schet']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО',
                'style': 'width: 500px'
            }),
            "phone": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Номер телефона',
                'style': 'width: 500px'
            }),
            "email": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'style': 'width: 500px'
            }),
            "date_burn": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата рождения',
                'style': 'width: 170px'
            }),
            "pasport": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Серия и номер паспорта',
                'style': 'width: 250px'
            }),
            "pasport_otdel": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Кем выдан',
                'style': 'width: 500px'
            }),
            "pasport_code": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Код подразделения',
                'style': 'width: 250px'
            }),
            "date_pasport": DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Дата выдачи',
                'style': 'width: 170px'
            }),
            "registr": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Место регистрации',
                'style': 'width: 500px'
            }),
            "organisation": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Полное наименование организации',
                'style': 'width: 500px'
            }),
            "inn": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ИНН',
                'style': 'width: 250px'
            }),
            "ogrn": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ОГРН',
                'style': 'width: 250px'
            }),
            "name_bank": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Название банка',
                'style': 'width: 250px'
            }),
            "bik": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Бик банка',
                'style': 'width: 250px'
            }),
            "schet": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Номер счета',
                'style': 'width: 250px'
            }),
            "korp_schet": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Корпоративный счет',
                'style': 'width: 250px'
            })
        }