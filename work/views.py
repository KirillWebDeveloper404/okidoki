from django.conf.urls import url
from django.core.files.base import File
from django.http.response import HttpResponse, JsonResponse
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
import qrcode
from django.conf import settings
from threading import Timer
from .utils import *


def work(req, page, message = None):
    try:
        if message:
            messages = [message]
        else:
            messages = []
        if req.method == 'POST':
            if 'addTemplate' in req.POST:
                form = TemplateUpload(req.POST, req.FILES, instance=req.user)
                if form.is_valid():
                    if create_template(form, req):
                        messages.append("Шаблон успешно добавлен!")
                    else:
                        messages.append("Ошибка! Проверьте правильность заполнения формы.")
            
            if 'verEmail' in req.POST:
                code = auth.send_sms(req.user.phone)
                send_email(subject="Подтвердите Email", recipients=[req.user.email], text=f"Для подтверждения перейдите по ссылке {req.build_absolute_uri().replace('settings', 'verEmail' + '/' + str(code))}")
                messages.append('Письмо для подтверждения отправлено на почту:<br>' + req.user.email)

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
                    signatures.append(signatured[i])
        
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

    except Exception as e:
        print(e)
        return redirect('main')


def verEmail(req, code):
    if req.user.is_authenticated:
        user = auth.authenticate(req.user.phone, code)
        if user:
            user.verEmail = True
            user.save()
            return render(req, 'work/work.html', 
        {
            'page': 'settings',
            'user': user,
            'messages': ['Почта подтверждена!']
        })
    else:
        return redirect('home')


def editDoc(req, id):
    messages = []
    saveEditor = ''
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

                if have_all_directives:
                    file_path = str(document.file.path).replace("\\", '/')
                    f = open(file_path, "rb")
                    html = mammoth.convert_to_html(f)

                    data = {}

                    for directive in directives:
                        data[str(directive['name'])] = req.POST[str(directive['name'])]

                    for directive in system_directives:
                        data[str(directive['name'])] = '{{' + str(directive['name']) + '}}'

                    file = DocxTemplate(file_path)
                    file.render(data)
                    file_path_ = file_path.replace('templates', 'signatured')

                    try:
                        print(file_path_)
                        os.makedirs(file_path_.replace(file_path_.split('/')[-1], ''))
                    except Exception as e:
                        print(e)

                    file.save(file_path_)
                    file = open(file_path_, 'rb')

                    signature = SignatureDocx()
                    signature.create(document)
                    signature.file = File(file, file_path_.split('/')[-1])
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
                    saveEditor = req.POST['saveEditor']

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
                        file_path = str(file_doc.file.path).replace("\\", '/')
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

                    if True:
                        document = Document()
                        new_parser = HtmlToDocx()
                        new_parser.add_html_to_document(html, document)
                        document.save(file_path)
                        return redirect("work", page="templates", message="Документ сохранён!")
                    else:
                        messages.append("Присутствуют не все директивы!")

        document = Template.objects.get(id = id)
        if document:
            file_path = str(document.file.path).replace("\\", '/')
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)

            form = DiretiveForm()

            directives = document.directive_set.all().values()
            textEditor = html.value

            if saveEditor != '':
                textEditor = saveEditor

            return render(req, 'work/editTemplate.html', 
            {
                'texts': textEditor,
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


def newDoc(req, id):
    messages = []
    urlSignature = ''
    system_directives = [
        {'name': 'current_date', 'desc': 'Текущая дата(подставляется автоматически)'},
        {'name': 'disclaimer', 'desc': 'дисклеймер'},
        {'name': 'client_name', 'desc': 'ФИО клиента'},
        {'name': 'client_phone', 'desc': 'Номер телефона клиента'},
        {'name': 'client_email', 'desc': 'E-mail клиента'}
    ]

    try:
        if req.method == 'POST':
            if 'signature' in req.POST:
                document = Template.objects.get(id=id)
                html = req.POST['template']
                have_all_directives = True
                directives = document.directive_set.all().values()

                if have_all_directives:
                    file_path = str(document.file.path).replace("\\", '/')
                    f = open(file_path, "rb")
                    html = mammoth.convert_to_html(f)

                    data = {}

                    for directive in directives:
                        data[str(directive['name'])] = req.POST[str(directive['name'])]

                    for directive in system_directives:
                        data[str(directive['name'])] = '{{' + str(directive['name']) + '}}'

                    file = DocxTemplate(file_path)
                    file.render(data)
                    file_path_ = file_path.replace('templates', 'signatured')

                    try:
                        print(file_path_)
                        os.makedirs(file_path_.replace(file_path_.split('/')[-1], ''))
                    except Exception as e:
                        print(e)

                    file.save(file_path_)
                    file = open(file_path_, 'rb')

                    signature = SignatureDocx()
                    signature.create(document)
                    signature.file = File(file, file_path_.split('/')[-1])
                    signature.save()
                    urlSignature = str(req.build_absolute_uri().replace('editTemplate', 'signature')).replace('/' + str(id), '/' + str(signature.id)).replace('newDoc', 'signature').split('?')[0]
                    img = qrcode.make(urlSignature)
                    path_img = os.path.join(settings.BASE_DIR, 'static/img/qr.png')
                    img.save(path_img)
                    messages.append("Договор выставлен на подпись. Ссылка скопирована в буффер обмена:<br>" + urlSignature + """<br><img src="/static/img/qr.png" style="transform: scale(0.75); margin: 0 -25px;">""")
                    delete_link_after_20_min = Timer(60.0*20.0, delete, [signature])
                    delete_link_after_20_min.start()
                    
                    document = Template.objects.get(id = id)
                    if document:
                        file_path = str(document.file.path).replace("\\", '/')
                        file_path = os.path.join(settings.BASE_DIR, file_path)
                        f = open(file_path, "rb")
                        html = mammoth.convert_to_html(f)

                        form = DiretiveForm()

                        directives = document.directive_set.all().values()

                        return render(req, 'work/newDoc.html', 
                        {
                            'texts': html.value,
                            'name': document.name,
                            'id': document.id,
                            'form': form,
                            'directives': directives,
                            'system_directives': system_directives,
                            'open': '{{',
                            'close': '}}',
                            'messages': messages,
                            'urlSignature': urlSignature
                        })

        document = Template.objects.get(id = id)
        if document:
            file_path = str(document.file.path).replace("\\", '/')
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)

            form = DiretiveForm()

            directives = document.directive_set.all().values()

            return render(req, 'work/newDoc.html', 
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
            return render(req, 'work/newDoc.html', 
            {
                'messages': ["Такого шаблона не существует. Проверьте правильность url или загрузите шаблон заново!"]
            })

    except Exception as e:
        print(traceback.format_exc(1))
        return render(req, 'work/newDoc.html', 
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
                    file_path = str(document.file.path).replace("\\", '/')

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
                    os.makedirs(file_path_.replace(file_path_.split('/')[-1], ''))
                except:
                    pass

                file.save(file_path_)
                file = open(file_path_, 'rb')
                signatured_doc = document
                signatured_doc.client = req.user
                signatured_doc.file = File(file, file_path_.split('/')[-1])
                signatured_doc.save()
                html = mammoth.convert_to_html(file)
                template = Template.objects.get(id = signatured_doc.template_id)

                client = req.user
                commers = User.objects.get(id = template.user_id)

                send_email(subject=f"Договор с {commers.name}", recipients=[client.email], text='Договор подписан!', filepath=signatured_doc.file.path)
                send_email(subject=f"Договор с {client.name}", recipients=[commers.email], text='Договор подписан!', filepath=signatured_doc.file.path)

                return render(req, 'work/view.html', {
                    'messages': ['Договор подписан!'],
                    'text': html.value
                })

        document = SignatureDocx.objects.get(id = id)
        if document:
            file_path = str(document.file.path).replace("\\", '/')
            file_path = os.path.join(settings.BASE_DIR, file_path)
            f = open(file_path, "rb")
            html = mammoth.convert_to_html(f)
            text = str(html.value)

            text = text.replace('{{current_date}}',  datetime.date.today().strftime("%d.%m.%Y"))
            text = text.replace('{{disclaimer}}', 'Дисклеймер(будет доделано позже)')
            text = text.replace('{{client_name}}', req.user.name)
            text = text.replace('{{client_phone}}',  req.user.phone)
            text = text.replace('{{client_email}}',  req.user.email)
            
        return render(req, 'work/signature.html', 
                {
                    'text': text
                })

    else:
        return redirect("login", next='signatureTemplate', page=id)


def view(req, id):
    if req.user.is_authenticated:

        document = SignatureDocx.objects.get(id = id)
        tpl = Template.objects.get(id = document.template_id)

        is_client = document.client == req.user
        is_owner = tpl.user == req.user

        if document:
            file_path = str(document.file.path).replace("\\", '/')
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


def downloadTemplate(req, id):
    if req.user.is_authenticated:
        template = Template.objects.get(id = id)
        file_path = template.file.path
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = f'inline; filename={template.name}.docx' + os.path.basename(file_path)
        return response

    else:
        return redirect('home')


def downloadSignature(req, id):
    if req.user.is_authenticated:
        template = SignatureDocx.objects.get(id = id)
        file_path = template.file.path
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = f'inline; filename={template.template.name}.docx'
        return response

    else:
        return redirect('home')