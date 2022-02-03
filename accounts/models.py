from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(verbose_name="Name", max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone", max_length=100, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=100, blank=True, null=True)
    verEmail = models.BooleanField(verbose_name="Верификация email", blank=True, null=True)
    date_burn = models.DateField(verbose_name="birthday", blank=True, null=True)
    pasport = models.CharField(verbose_name="pasport's seria and number", max_length=20, blank=True, null=True)
    pasport_otdel = models.CharField(verbose_name="who gives pasport", max_length=250, blank=True, null=True)
    pasport_code = models.CharField(verbose_name="pasport code", max_length=50, blank=True, null=True)
    date_pasport = models.DateField(verbose_name="pasport date", blank=True, null=True)
    registr = models.TextField(verbose_name="from", blank=True, null=True)
    organisation = models.CharField(verbose_name="full organisation name", max_length=200, blank=True, null=True)
    inn = models.CharField(max_length=100, blank=True, null=True)
    ogrn = models.CharField(max_length=100, blank=True, null=True)
    name_bank = models.CharField(max_length=100, blank=True, null=True)
    bik = models.CharField(max_length=100, blank=True, null=True)
    schet = models.CharField(max_length=100, blank=True, null=True)
    korp_schet = models.CharField(max_length=100, blank=True, null=True)

    code = models.CharField(max_length=10, blank=True, null=True)

    def create(self, data):
        self.name = data['name']
        self.phone = str(data['phone']).replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
        self.email = data['email']
        self.username = data['email'].replace('.', '')
        self.date_burn = data['date_burn']
        self.pasport = data['pasport']
        self.pasport_otdel = data['pasport_otdel']
        self.pasport_code = data['pasport_code']
        self.date_pasport = data['date_pasport']
        self.registr = data['registr']
        self.organisation = data['organisation']
        self.inn = data['inn']
        self.ogrn = data['ogrn']
        self.name_bank = data['name_bank']
        self.bik = data['bik']
        self.schet = data['schet']
        self.korp_schet = data['korp_schet']
        return self

    def __str__(self):
        if self.name:
            return self.name
        elif self.username:
            return str(self.username) + '(админ)'
    

    class Meta:
        managed=True
        verbose_name = 'User'
        verbose_name_plural = 'Users'