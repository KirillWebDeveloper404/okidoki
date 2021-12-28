from django.forms.widgets import FileInput, TextInput, Textarea
from .models import SignatureDocx, Template, Directive
from django.forms import ModelForm


class TemplateUpload(ModelForm):

    class Meta:
        model = Template
        fields = ['name', 'file']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Название шаблона',
                'name': 'name'
                # 'style': 'width: 750px'
            }),
            "file": FileInput(attrs={
                'type': 'file',
                'class': 'form-control mt-3',
                'placeholder': 'Выберите файл',
                'name': 'file',
                 'data-ajax': "false"
            })
        }


class DiretiveForm(ModelForm):

    class Meta:
        model = Directive
        fields = ['name', 'desc']

        widgets = {
            "name": TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Название директивы',
                'name': 'name',
                'id': 'name'
                # 'style': 'width: 750px'
            }),
            "desc": Textarea(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Описание',
                'name': 'desc',
                'id': 'desc'
            }),
        }


class SignatureForm(ModelForm):

    class Meta:
        model = SignatureDocx
        fields = ['template', 'client', 'file']