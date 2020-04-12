import time

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/changecartstate/',
    '/axf/allselect/',
    '/axf/makeorder/'
]

REQUIRE_LOGIN = [
    '/axf/cart/',
    '/axf/orderdetail/',
    '/axf/orderlistnotpay/',
    '/axf/orderlistnotreceive/'
]

RATE_REQUEST = [
    '/axf/verifypassword/'
]

class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if request.path in REQUIRE_LOGIN_JSON:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user
                except:
                    data = {'status':302,'msg':'user is not avaliable'}
                    return JsonResponse(data=data)
            else:
                data = {'status':302,'msg':'user not login'}
                return JsonResponse(data=data)

        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user
                except:
                    return redirect(reverse('axf:login'))
            else:
                return redirect(reverse('axf:login'))


class ReateMiddele(MiddlewareMixin):
    def process_request(self,request):
        if request.path in RATE_REQUEST:
            ip =request.META.get('REMOTE_ADDR')
            requests = cache.get(ip)
            if requests:
                wait = int(60 - (time.time() - requests))
                return JsonResponse({'status':400,'msg':wait})
            requests = time.time()
            cache.set(ip,requests,timeout=60)