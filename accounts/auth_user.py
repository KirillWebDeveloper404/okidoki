from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
import random
from .models import User


class UserAuth(ModelBackend):
    
    def send_sms(phone):
        try:
            code = str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))
            code = 123456
            user = User.objects.get(phone=phone)
            user.code = code
            print(code)
            user.save()
            return True
        except Exception as e:
            return None

    def authenticate(phone=None, code=None, username=None, email=None, password=None):
        try:
            if username != None:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    return user

            elif phone != None:
                user = User.objects.get(phone=phone)
                if user != None and code == user.code:
                    return user

            elif email != None:
                user = User.objects.get(email=email)
                if check_password(user.password, password):
                    return user

            return None

        except Exception as e:
            print(e)
            return None