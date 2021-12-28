from re import template
from django.db import models
from accounts.models import User


def content_file_name(instance, filename):
    return '/'.join(['templates', instance.user.username, filename])

class Template(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    file = models.FileField(verbose_name="Шаблон", upload_to=content_file_name)

    def create(self, data):
        self.user = data['id']
        self.name = data['name']
        self.file = data['file']

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
        self.name = data['name']
        self.desc = data['desc']

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        verbose_name = 'Directive'
        verbose_name_plural = 'Directives'


class SignatureDocx(models.Model):

    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    file = models.FileField(verbose_name="Подписанный докумет", upload_to='/'.join(['content']), blank=True, null=True)

    def create(self, data):
        self.template = data

    class Meta:
        managed = True
        verbose_name = 'SignatueDocx'
        verbose_name_plural = 'SignatueDocxs'