from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparam/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<sortid>\d+)/', views.market_with_param,
        name='market_with_param'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^forget/', views.forget, name='forget'),
    url(r'^verifypassword/', views.verify_password, name='verify_password'),
    url(r'^verifycode/', views.verifycode, name='verifycode'),
    url(r'^checkuser/', views.checkuser, name='checkuser'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^activate/', views.activate, name='activate'),
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),
    url(r'^allselect/', views.all_select, name='all_select'),
    url(r'^makeorder/', views.make_order, name='make_order'),
    url(r'^orderdetail/', views.order_detail, name='order_detail'),
    url(r'^orderlistnotpay/', views.orderlist_not_pay, name='orderlist_not_pay'),
    url(r'^orderlistnotreceive/', views.orderlist_not_receive, name='orderlist_not_receive'),
    url(r'^alipay/', views.alipay, name='alipay'),
    url(r'^check_alipay/', views.check_alipay, name='check_alipay'),


]