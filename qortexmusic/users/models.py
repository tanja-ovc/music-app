'''
Для возможности дальнейшей расширяемости проекта создаю модель User,
а её в свою очередь тоже делаю расширяемой на будущее в соответствии с
доументацией:
https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
'''
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
