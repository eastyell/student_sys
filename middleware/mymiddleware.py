import time
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print("中间件方法 process_request 被调用")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("中间件方法 process_view 被调用")

    def process_response(self, request, response):
        print("中间件方法 process_response 被调用")
        return response

    def process_exception(self, request, exception):
        print("中间件方法 process_exception 被调用")

    def process_template_response(self, request, response):
        print("中间件方法 process_template_response 被调用")
        return response


# 限制用户访问次数,每60秒不超过5次
# 构建访问者IP池
visit_ip_pool = {}  # 以'ip'地址为键，以访问的网站的时间戳列表作为值形如{'127.0.0.1':[时间戳,...]}


class VisitLimitMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            print(request.method)
            # 获取用户的访问的ip地址
            ip = request.META.get("REMOTE_ADDR")
            print('ip', ip)
            # 获取访问时间
            visit_time = time.time()
            if ip not in visit_ip_pool:
                # 护字典,将新的ip地址加入字典
                visit_ip_pool[ip] = [visit_time]
            else:
                # 已经存在，则将ip对应值的插入列表开始位置
                visit_ip_pool[ip].insert(0, visit_time)
            # 获取ip_list列表
            ip_list = visit_ip_pool[ip]
            # 计算访问时间差
            lead_time = ip_list[0] - ip_list[-1]
            print('地址:', ip, '访问次数:', len(ip_list), '时间差', lead_time)
            # 两个条件同时成立则，间隔时间在60s内
            while ip_list and lead_time > 60:
                # 默认移除列表中的最后一个元素,重新开始计算
                ip_list.pop()
            # 间隔在60s内判断列表的长度即访问的次数是否大于5次
            if len(ip_list) > 10:
                return HttpResponse("对不起，操作次数过于频繁，将终止你的操作请求...")
            print('地址:', ip, '访问次数:', len(ip_list), '时间差', lead_time)