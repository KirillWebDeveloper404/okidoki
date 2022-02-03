from re import template
from django.db import models
from accounts.models import User


def content_file_name(instance, filename):
    return '/'.join(['templates', instance.user.username, filename])

class Template(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    file = models.FileField(verbose_name="Шаблон", upload_to=content_file_name)

    is_exist = models.BooleanField(verbose_name="удаление", blank=True, default=True)

    def create(self, data):
        self.user = data['id']
        self.name = data['name']
        self.file = data['file']
        self.is_exist = True

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed=True
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'


class Directive(models.Model):

    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    desc = models.TextField()

    def create(self, data):
        self.template = data['template']
        self.name = str(data['name']).replace(' ', '_')
        self.desc = data['desc']

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Directive'
        verbose_name_plural = 'Directives'


class SystemDirective(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название которое увидят пользователи')
    desc = models.TextField(verbose_name='Описание которое увидят пользователи')
    default_value = models.TextField(verbose_name='Значение подставляющиеся автоматически', blank=True, default='')

    def create(self, data):
        self.name = data['name']
        self.desc = data['desc']

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        verbose_name = 'SystemDirective'
        verbose_name_plural = 'SystemDirectives'


class SignatureDocx(models.Model):

    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    file = models.FileField(verbose_name="Подписанный докумет", upload_to='signatured/', blank=True, null=True)

    def create(self, data):
        self.template = data

    class Meta:
        managed = True
        verbose_name = 'SignatueDocx'
        verbose_name_plural = 'SignatueDocxs'