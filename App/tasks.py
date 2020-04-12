from celery import shared_task
from django.core.mail import send_mail
from django.template import loader

from GPAXF.settings import SERVER_HOST, SERVER_PORT, EMAIL_HOST_USER


@shared_task
def send_email_activate(username,recipient,u_token):
    subject = 'AXF ACTIVATE'
    data ={
        'username':username,
        'activate_url':'http://{}:{}/axf/activate/?u_token={}'.format(SERVER_HOST,SERVER_PORT,u_token)
    }
    html_message = loader.get_template('user/activate.html').render(data)

    from_email = EMAIL_HOST_USER
    recipient_list = [recipient]
    send_mail(subject=subject,from_email=from_email,message='',html_message=html_message,recipient_list=recipient_list)

@shared_task
def send_email_password(username,recipient,veifycode):
    subject = 'AXF RESET PASSWORD'
    data = {
        'username': username,
        'verifycode': veifycode
    }
    html_message = loader.get_template('user/verify_password.html').render(data)

    from_email = EMAIL_HOST_USER
    recipient_list = [recipient]
    send_mail(subject=subject, from_email=from_email, message='', html_message=html_message,
              recipient_list=recipient_list)
