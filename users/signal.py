import django.dispatch
from django.dispatch import receiver


#创建一个信号
from users.models import User

login_signal = django.dispatch.Signal()  # 触发的时候需要传递的参数


# 定义回调函数(即信号接收者)并使用装饰器进行注册
@receiver(login_signal, dispatch_uid="register_callback")
def register_callback(sender, **kwargs):
    print("用户：%s，在客户端IP地址：%s 成功登录！" % (kwargs['user'].userName, kwargs['request'].META['REMOTE_ADDR']))