from django.core.files.base import File
from django.shortcuts import redirect, render
from accounts.models import User
from work.forms import DiretiveForm, TemplateUpload
from work.models import Directive, SignatureDocx, Template
import mammoth
from docx import Document
from htmldocx import HtmlToDocx
from django.conf import settings
import os
import datetime
from docxtpl import DocxTemplate
from accounts.auth_user import UserAuth as auth
import traceback


def work(req, page):
    try:
        messages = []
        if req.method == 'POST':
            form = TemplateUpload(req.POST, req.FILES, instance=req.user)
            if form.is_valid():
                try:
                    template = Template()
                    data = form.cleaned_data
                    data['id'] = req.user

                    template.create(data)
                    template.save()
                    messages.append("Шаблон успешно добавлен!")
                except Exception as e:
                    messages.append("Ошибка! Проверьте правильность заполнения формы.")

        user = User.objects.get(phone=req.user.phone)
        templates = user.template_set.all().values()
        form = TemplateUpload()

        signatures = []

        for template in user.template_set.all():
            signatured = template.signaturedocx_set.all().values()
            for i, el in enumerate(signatured):
                if el['client_id']:
                    signatured[i]['name'] = Template.objects.get(id = el['template_id']).name
                    signatured[i]['user_name'] = User.objects.get(id = int(el['client_id'])).name
                    signatures.append(signatured)
        
        if len(signatures) == 0:
            for signatured in user.signaturedocx_set.all().values():
                signatured['name'] = Template.objects.get(id = signatured['template_id']).name
                signatured['user_name'] = Template.objects.get(id = signatured['template_id']).user
                signatures.append(signatured)

            return render(req, 'work/work.html', 
            {
                'page': page,
                'user': user,
                'templates': templates,
                'signatures': [signatures],
                'form': form,
                'messages': messages
            })

        if len(signatures) == 0:
            return render(req, 'work/work.html', 
            {
                'page': page,
                'user': user,
                'templates': templates,
                'signatures': [],
                'form': form,
                'messages': messages
            })

        else:
            return render(req, 'work/work.html', 
            {
                'page': page,
                'user': user,
                'templates': templates,
                'signatures': [signatures[0]],
                'form': form,
                'messages': messages
            })

    except Exception as e:
        print(e)
        return redirect('main')


def editDoc(req, id):
    messages = []
    system_directives = [
        {'name': 'current_date', 'desc': 'Текущая дата(подставляется автоматически)'},
        {'name': 'disclaimer', 'desc': 'дисклеймер'},
        {'name': 'client_name', 'desc': 'ФИО клиента'},
        {'name': 'client_phone', 'desc': 'Номер телефона клиента'},
        {'name': 'client_email', 'desc': 'E-mail клиента'}
    ]

    try:
        if req.method == 'POST':
            print(req.POST)
            if 'signature' in req.POST:
                document = Template.objects.get(id=id)
                html = req.POST['template']
                have_all_directives = True
                directives = document.directive_set.all().values()

                for directive in directives:
                    if not (str(directive['name']) in html):
                        have_all_directives = False

                for directive in system_directives:
                    if not (str(directive['name']) in html):
                        have_all_directives = False
                        messages.append("Присутствуют не все директивы!")
                if have_all_directives:
                    file_path = str(document.file.path)
                    f = open(file_path, "rb")
                    html = mammoth.convert_to_html(f)

                    data = {}

                    for directive in directives:
                        data[str(directive['name'])] = req.POST[str(directive['name'])]

                    for directive in system_directives:
                        data[str(directive['name'])] = '{{' + str(directive['name']) + '}}'

                    file = DocxTemplate(file_path)
                    file.render(data)
                    file_path_ = file_path.replace('templates', 'signatures')

                    try:
                        os.makedirs(file_path_.replace(file_path_.split('\\')[-1], ''))
                    except Exception as e:
                        print(e)

                    file.save(file_path_)
                    file = open(file_path_, 'rb')

                    signature = SignatureDocx()
                    signature.create(document)
                    signature.file = File(file, file_path_.split('\\')[-1])
                    signature.save()
                    messages.append("Договор выставлен на подпись. Скопируйте ссылку и передайте клиенту: " + str(req.build_absolute_uri().replace('editTemplate', 'signature')).replace('/' + str(id), '/' + str(signature.id)).split('?')[0])
                    

            if 'directive' in req.POST:
                form = DiretiveForm(req.POST, instance=req.user)
                if form.is_valid():
                    directive = Directive()
                    data = {}
                    data['name'] = req.POST['name']
                    data['desc'] = req.POST['desc']
                    data['template'] = Template.objects.get(id = id)
                    directive.create(data)
                    directive.save()

            if 'directive_edit' in req.POST:
                id_directive = req.POST['id']
                directive = Directive.objects.get(id=id_directive)
                directive.name = req.POST['name']
                directive.desc = req.POST['desc']
                directive.save()

            if 'directive_delete' in req.POST:
                id_directive = req.POST['id']
                directive = Directive.objects.get(id=id_directive)
                directive.delete()

            if 'editor' in req.POST:
                if req.POST['editor']:
                    file_doc = Template.objects.get(id = id)
                    if file_doc:
                        file_path = str(file_doc.file.path)
                        file_path = os.path.join(settings.BASE_DIR, file_path)
                    html = req.POST['editor']

                    have_all_directives = True

                    document = Template.objects.get(id = id)
                    directives = document.directive_set.all().values()

                    for directive in directives:
                        if not (str(directive['name']) in html):
                            have_all_directives = False

                    for directive in system_directives:
                        if not (str(directive['name']) in html):
                            have_all_directives = False

                    if have_all_directives:
                        document = Document()
                        new_parser = HtmlToDocx()
                        new_parser.add_html_to_document(html, document)
                        document.save(file_path)
                        messages.append("Документ сохранён!")
                    else:
                        messages.append("Присутствуют не все директивы!")

        document = Template.objects.get(id = id)
        if document:
            file_path = str(document.file.path)
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)

            form = DiretiveForm()

            directives = document.directive_set.all().values()

            return render(req, 'work/editTemplate.html', 
            {
                'texts': html.value,
                'name': document.name,
                'id': document.id,
                'form': form,
                'directives': directives,
                'system_directives': system_directives,
                'open': '{{',
                'close': '}}',
                'messages': messages
            })
        else:
            return render(req, 'work/editTemplate.html', 
            {
                'messages': ["Такого шаблона не существует. Проверьте правильность url или загрузите шаблон заново!"]
            })

    except Exception as e:
        print(traceback.format_exc(1))
        return render(req, 'work/editTemplate.html', 
            {
                'messages': ["Такого шаблона не существует. Проверьте правильность url или загрузите шаблон заново!"]
            })


def signatureDoc(req, id):
    sign_doc = SignatureDocx.objects.get(id = id)

    if req.user.is_authenticated and not(sign_doc.client_id):
        if not('sms' in req.POST):
            auth.send_sms(req.user.phone)
        if 'sms' in req.POST:
            res = auth.authenticate(req.user.phone, req.POST['sms'])
            if res != None:
                document = SignatureDocx.objects.get(id = id)
                print(document)
                if document:
                    file_path = str(document.file.path)

                    file_path = os.path.join(settings.BASE_DIR, file_path)
                    f = open(file_path, "rb")
                    html = mammoth.convert_to_html(f)

                data = {}

                data['current_date'] = datetime.date.today().strftime("%d.%m.%Y")
                data['disclaimer'] = 'Дисклеймер(будет доделано позже)'
                data['client_name'] = req.user
                data['client_phone'] = req.user.phone
                data['client_email'] = req.user.email

                file = DocxTemplate(file_path)
                file.render(data)
                file_path_ = file_path

                try:
                    os.makedirs(file_path_.replace(file_path_.split('\\')[-1], ''))
                except:
                    pass

                file.save(file_path_)
                file = open(file_path_, 'rb')
                signatured_doc = document
                signatured_doc.client = req.user
                signatured_doc.file = File(file, file_path_.split('\\')[-1])
                signatured_doc.save()
                html = mammoth.convert_to_html(file)

                return render(req, 'work/view.html', {
                    'messages': ['Договор подписан!'],
                    'text': html.value
                })

        document = SignatureDocx.objects.get(id = id)
        if document:
            file_path = str(document.file.path)
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)
            
        return render(req, 'work/signature.html', 
                {
                    'text': html.value
                })

    else:
        return redirect("main")


def view(req, id):
    if req.user.is_authenticated:

        document = SignatureDocx.objects.get(id = id)
        tpl = Template.objects.get(id = document.template_id)

        is_client = document.client == req.user
        is_owner = tpl.user == req.user

        if document:
            file_path = str(document.file.path)
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)
            
        if is_client or is_owner:
            return render(req, 'work/view.html', 
                    {
                        'text': html.value
                    })
        else:
            return redirect('work', 'settings')

    else:
        return redirect("main")
