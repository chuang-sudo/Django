import uuid

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import random

# Create your views here.
from django.urls import reverse

from App.models import MainWheel, AXFUser, FoodType, Goods, Cart, Order, OrderGoods
from App.tasks import send_email_activate, send_email_password
from App.views_constant import HTTP_USER_EXIST, ALL_TYPE, PRICE_HIGH, PRICE_LOW, SELL_HIGH, ORDER_STATUS_NOT_PAY, \
    ORDER_STATUS_NOT_RECEIVE
from App.views_helper import hash_str, get_total_price
from GPAXF.settings import MEDIA_KEY_PREFIX, ALIPAY_PRIVATE_KEY, ALIPAY_PUBLIC_KEY, ALIPAY_APPID


def home(request):
    main_wheels = MainWheel.objects.all()
    data = {
        'title': '首页',
        'main_wheels': main_wheels
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_param', kwargs={'typeid': 104749, 'childcid': 0, 'sortid': 0}))


def market_with_param(request, typeid, childcid, sortid):
    user_id = request.session.get('user_id')

    foodtypes = FoodType.objects.all()
    foodtype = foodtypes.get(typeid=typeid)

    good_list = Goods.objects.filter(categoryid=typeid)
    for good in good_list:

        carts = good.cart_set.filter(c_user_id=user_id)

        if carts:
            cart = carts.first()
            good.num = cart.c_goods_nums

    if childcid == '0':
        # print(1)
        pass
    else:
        good_list = good_list.filter(childcid=childcid)

    if sortid == ALL_TYPE:
        pass
    elif sortid == PRICE_HIGH:
        good_list = good_list.order_by('-price')
        # print(2)
    elif sortid == PRICE_LOW:
        good_list = good_list.order_by('price')
    elif sortid == SELL_HIGH:
        good_list = good_list.order_by('productnum')

    """全部分类:0#进口水果:103534#国产水果:103533
        切割#[全部分类:0,进口水果:103534,国产水果:103533]
        切割:[[全部分类,0],[进口水果,103534],[国产水果,103533]]
    """
    childtypenames = foodtype.childtypenames

    foodtype_childtypenames_list = childtypenames.split('#')
    foodtype_childtypenames_list_list = []

    for foodtype_childnames in foodtype_childtypenames_list:
        foodtype_childtypenames_list_list.append(foodtype_childnames.split(':'))

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'good_list': good_list,
        'typeid': int(typeid),
        'childcid': childcid,
        'sortid': sortid,
        'foodtype_childtypenames_list_list': foodtype_childtypenames_list_list
    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)

    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
    # price_list = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    # sum_price = total_price(price_list)
    data = {
        'carts': carts,
        'title': '购物车',
        'is_all_select': is_all_select,
        'sum_price': get_total_price(Cart.objects.filter(c_user=request.user).filter(c_is_select=True))
    }
    return render(request, 'main/cart.html', context=data)


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册'
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        user = AXFUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon

        user.save()
        u_token = uuid.uuid4().hex
        print(u_token)
        cache.set(u_token, user.id, timeout=60 * 60 * 24)
        send_email_activate.delay(username, email, u_token)
        return render(request, 'user/login.html')


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect(reverse('axf:login'))
    return render(request, 'user/activate_fail.html')


def login(request):
    data = {}
    if request.method == 'GET':
        data['title'] = '登录'
        return render(request, 'user/login.html', context=data)
    elif request.method == 'POST':
        verifycode = request.POST.get('verifycode')
        verifycode = verifycode.lower()
        rand_str = request.session.get('rand_str').lower()
        if verifycode != rand_str:
            data['erro_message'] = '验证码错误'
            return render(request, 'user/login.html', context=data)
        # 核对用户名，密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)

        users = AXFUser.objects.filter(u_username=username) or AXFUser.objects.filter(u_email=username)

        if users.exists():
            user = users.first()
            if check_password(password, user.u_password):

                request.session['user_id'] = user.id
                return redirect(reverse('axf:mine'))
            else:
                data['erro_message'] = '密码错误'

                return render(request, 'user/login.html', context=data)

        data['erro_message'] = '用户不存在'

        return render(request, 'user/login.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': False
    }

    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['is_active'] = user.is_active
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_RECEIVE).count()

    return render(request, 'main/mine.html', context=data)


def checkuser(request):
    username = request.GET.get('username')
    users = AXFUser.objects.filter(u_username=username) or AXFUser.objects.filter(u_email=username)
    data = {
        "status": 200,
        "message": "user can use",
    }
    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['message'] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def add_to_cart(request):
    user = request.user
    good_id = request.POST.get('g_id')
    good = Goods.objects.get(id=good_id)

    opreate_type = request.POST.get('opreate_type')

    carts = Cart.objects.filter(c_user=user).filter(c_goods=good)

    if carts.exists():
        cart = carts.first()
        if opreate_type == 'add':
            cart.c_goods_nums = cart.c_goods_nums + 1

        elif opreate_type == 'sub':
            cart.c_goods_nums = cart.c_goods_nums - 1
    else:
        cart = Cart()
        cart.c_user = user
        cart.c_goods = good
    cart.save()

    data = {'status': 200, 'msg': 'ok', 'num': cart.c_goods_nums}
    return JsonResponse(data=data)


def change_cart_state(request):
    user = request.user
    operate_type = request.POST.get('o_type')
    cart_id = request.POST.get('c_id')
    cart_obj = Cart.objects.get(pk=cart_id)

    if (operate_type == 'change'):
        cart_obj.c_is_select = not cart_obj.c_is_select
    elif (operate_type == 'add'):
        cart_obj.c_goods_nums = cart_obj.c_goods_nums + 1
    elif (operate_type == 'sub'):
        cart_obj.c_goods_nums = cart_obj.c_goods_nums - 1
    cart_obj.save()
    if cart_obj.c_goods_nums == 0:
        cart_obj.delete()

    is_all_select = not Cart.objects.filter(c_user=user).filter(c_is_select=False).exists()

    # price_list = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    # sum_price = total_price(price_list)

    data = {
        'status': 200,
        'msg': 'change cart sate',
        'is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'num': cart_obj.c_goods_nums,
        'sum_price': get_total_price(Cart.objects.filter(c_user=request.user).filter(c_is_select=True))
    }
    return JsonResponse(data=data)


def all_select(request):
    user = request.user
    cart_list = request.POST.get('cart_list').split('#')
    for cart_id in cart_list:
        cart_obj = Cart.objects.get(pk=cart_id)
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()
    is_all_select = not Cart.objects.filter(c_user=user).filter(c_is_select=False).exists()

    # price_list = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    # sum_price = total_price(price_list)
    data = {
        'status': 200,
        'msg': 'allselect success',
        'cart_list': cart_list,
        'is_all_select': is_all_select,
        'sum_price': get_total_price(Cart.objects.filter(c_user=request.user).filter(c_is_select=True))
    }

    return JsonResponse(data=data)


def make_order(request):
    order = Order()
    order.o_user = request.user
    order.o_price = get_total_price(Cart.objects.filter(c_user=request.user).filter(c_is_select=True))
    order.save()

    cart_list = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    for cart in cart_list:
        ordergoods = OrderGoods()
        ordergoods.og_order = order
        ordergoods.og_goods = cart.c_goods
        ordergoods.og_goods_num = cart.c_goods_nums
        ordergoods.save()
        cart.delete()

    data = {
        'status': 200,
        'msg': 'ok',
        'orderid': order.id
    }
    return JsonResponse(data=data)


def order_detail(request):
    order_id = request.GET.get('orderid')
    order = Order.objects.get(pk=order_id)
    data = {
        'title': '订单详情',
        'order': order,

    }
    return render(request, 'order/order_detail.html', context=data)


def orderlist_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)
    data = {
        'title': '待付款',
        'orders': orders
    }
    return render(request, 'order/orderlist_not_pay.html', context=data)


def orderlist_not_receive(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_RECEIVE)
    data = {
        'title': '待付款',
        'orders': orders
    }
    return render(request, 'order/orderlist_not_receive.html', context=data)


def alipay(request):
    total_price = request.GET.get('total_price')

    # Alipay Client
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'

    alipay_client_config.app_id = ALIPAY_APPID
    alipay_client_config.app_private_key = ALIPAY_PRIVATE_KEY
    alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000526"
    model.total_amount = total_price
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"

    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    # print("alipay.trade.page.pay response:" + response)
    return redirect(response)


def check_alipay(request):
    total_price = request.POST.get('total_price')
    data = {
        'status': 200,
        'total_price': total_price,
        'msg': 'success'
    }
    return JsonResponse(data=data)


def verifycode(request):
    # 定义变量，用于画面的背景色，宽，高
    bgColor = (random.randrange(20, 200), random.randrange(20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgColor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数和绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]

    # 构造字体对象
    font = ImageFont.truetype(r'‪C:\Windows\Fonts\arial.ttf', 40)
    # 构造字体颜色
    fontColor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontColor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontColor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontColor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制四个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontColor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontColor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontColor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontColor4)
    # 释放画笔
    del draw
    # 存入session，用于进一步验证
    request.session['rand_str'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存文件中
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def forget(request):
    if request.method == 'GET':
        data = {'title': '忘记密码'}
        return render(request, 'user/forget.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        verify_password = request.POST.get('verify_password')

        users = AXFUser.objects.filter(u_email=username) or AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            verify_password_code = cache.get(user.id)

            if verify_password == verify_password_code:
                user.u_password = make_password(password)
                user.save()
                print('ok')
                return redirect('axf:login')
        return redirect('axf:forget')


def verify_password(request):
    username = request.POST.get('username')
    users = AXFUser.objects.filter(u_email=username) or AXFUser.objects.filter(u_username=username)
    data = {}
    if users.exists():
        user = users.first()
        verify_password_code = ''
        for i in range(0, 4):
            verify_password_code += str(random.randint(0, 9))
            send_email_password.delay(user.u_username, user.u_email, verify_password_code)

            cache.set(user.id, verify_password_code, timeout=60 * 60 * 24)
            data = {'status': 200, 'msg': '已发送'}
    return JsonResponse(data=data)


