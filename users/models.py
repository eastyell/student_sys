from django.db import models


# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=24, verbose_name='用户名')
    passWord = models.CharField(max_length=24, verbose_name='密码')

    def __str__(self):
        return f'注册用户: {self.userName}'

    class Meta:
        verbose_name = verbose_name_plural = '用户信息'
