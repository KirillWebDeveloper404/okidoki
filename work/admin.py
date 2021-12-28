from django.contrib import admin

from work.models import SignatureDocx, Template, Directive


admin.site.register(Template)
admin.site.register(Directive)
admin.site.register(SignatureDocx)