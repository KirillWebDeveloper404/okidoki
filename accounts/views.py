from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .models import User
from .auth_user import UserAuth as auth


def register(req):
    step = 1
    messages = []
    if req.method == 'POST':
        regForm = UserRegisterForm(req.POST)
        if req.POST.get('close'):
            messages = []
        if regForm.is_valid() and '4' in req.POST.dict():
            if User.objects.filter(phone=regForm.cleaned_data['phone']):
                messages.append("Такой пользователь уже зарегистрирован!")
            else:
                data = regForm.cleaned_data
                user = User()
                user = user.create(data)
                user.save()
                auth.send_sms(req.POST.dict()['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', ''))
                messages.append("СМС отправлено!")
        else:
            if '2' in req.POST.dict():
                step = 2
            elif '3' in req.POST.dict():
                step = 3
        if '4' in req.POST.dict():
            step = 4

        elif '5' in req.POST.dict():
            user = auth.authenticate(req.POST.dict()['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', ''), req.POST.dict()['sms'])
            if user == None:
                messages.append("Неверный смс код или номер телефона")
            else:
                login(req, user)
                return redirect('work', page='settings')

    
    initial = {}

    data = [
        'name', 'phone', 'email',
        'pasport', 'pasport_otdel', 'pasport_code', 'date_pasport', 'registr', 'date_burn'
    ]

    for el in data:
        if el in req.POST.dict():
            initial[el] = req.POST.dict()[el]

    regForm = UserRegisterForm(initial=initial)
            
    return render(req, 'accounts/register.html', 
    {
        'form': regForm,
        'step': step,
        'messages': messages
    })

def registerClient(req):
    step = 1
    messages = []
    if req.method == 'POST':
        regForm = UserRegisterForm(req.POST)
        if req.POST.get('close'):
            messages = []
        if regForm.is_valid():
            if User.objects.filter(phone=regForm.cleaned_data['phone']):
                messages.append("Такой пользователь уже зарегистрирован!")

            elif 'send_sms' in req.POST.dict():
                step = 2
                data = regForm.cleaned_data
                data['phone'] = data['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
                user = User()
                user = user.create(data)
                user.save()
                auth.send_sms(req.POST.dict()['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', ''))

        if 'login' in req.POST.dict():
          user = auth.authenticate(req.POST.dict()['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', ''), req.POST.dict()['sms'])
          if user == None:
              messages.append("Неверный смс код или номер телефона")
          else:
              login(req, user)
              return redirect('work', page='settings')
    
    initial = {}

    data = [
        'name', 'phone', 'email',
        'pasport', 'pasport_otdel', 'pasport_code', 'date_pasport', 'registr', 'date_burn'
    ]

    for el in data:
        if el in req.POST.dict():
            initial[el] = req.POST.dict()[el]

    regForm = UserRegisterForm(initial=initial)
            
    return render(req, 'accounts/registerClient.html', 
    {
        'form': regForm,
        'messages': messages,
        'step': step
    })

def loginView(req):
    messages=[]
    if req.method == 'POST':
        data = req.POST.dict()
        print(data)
        if 'phone' in data and 'sms' not in data:
            res = auth.send_sms(str(data['phone']).replace(' ', '').replace('(', '').replace(')', '').replace('-', ''))
            if res:
                return render(req, 'accounts/login.html', 
                {
                    'sms': True,
                    'phone': str(data['phone']).replace(' ', '').replace('(', '').replace(')', '').replace('-', ''),
                    'messages': ["Смс отправлено!"]
                })
            else:
                return render(req, 'accounts/login.html', 
                {
                    'sms': False,
                    'messages': ["Неверный номер телефона!"]
                })
        
        if 'code' in data:
            user = auth.authenticate(req.POST.dict()['phone'], req.POST.dict()['sms'])
            if user == None:
                messages.append("Неверный смс код или номер телефона")
            else:
                login(req, user)
                return redirect('work', page='settings')

    return render(req, 'accounts/login.html', 
    {
        'sms': False,
        'messages': messages
    })

def logoutView(req):
    logout(req)
    return redirect('/')