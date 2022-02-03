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
                'id': 'name',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ФИО',
                'style': 'width: 500px'
            }),
            "phone": TextInput(attrs={
                'id': 'phone',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Номер телефона',
                'style': 'width: 500px'
            }),
            "email": TextInput(attrs={
                'id': 'email',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'style': 'width: 500px'
            }),
            "date_burn": DateInput(attrs={
                'id': 'date_burn',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Дата рождения',
                'style': 'width: 170px',
                'onfocus': '(this.type="date")'
            }),
            "pasport": TextInput(attrs={
                'id': 'pasport',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Серия и номер паспорта',
                'style': 'width: 250px'
            }),
            "pasport_otdel": TextInput(attrs={
                'id': 'pasport_otdel',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Кем выдан',
                'style': 'width: 500px'
            }),
            "pasport_code": TextInput(attrs={
                'id': 'pasport_code',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Код подразделения',
                'style': 'width: 250px'
            }),
            "date_pasport": DateInput(attrs={
                'id': 'date_pasport',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Дата выдачи',
                'style': 'width: 170px',
                'onfocus': '(this.type="date")'
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
                'id': 'inn',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ИНН',
                'style': 'width: 234px'
            }),
            "ogrn": TextInput(attrs={
                'id': 'ogrn',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'ОГРН',
                'style': 'width: 234px'
            }),
            "name_bank": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Название банка',
                'style': 'width: 234px'
            }),
            "bik": TextInput(attrs={
                'id': 'bik',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Бик банка',
                'style': 'width: 234px'
            }),
            "schet": TextInput(attrs={
                'id': 'schet',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Номер счета',
                'style': 'width: 234px'
            }),
            "korp_schet": TextInput(attrs={
                'id': 'korp_schet',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Корпоративный счет',
                'style': 'width: 234px'
            })
        }