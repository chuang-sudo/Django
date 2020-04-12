import hashlib

from django.core.mail import send_mail
from django.template import loader

from GPAXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


def hash_str(source):
    return hashlib.new('sha512',source.encode('utf-8')).hexdigest()


def get_total_price(list):
    total_price =0
    if list:
        for li in list:
            total_price = li.c_goods.price * li.c_goods_nums + total_price
    return total_price



