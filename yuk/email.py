from django.core.mail import send_mail, EmailMessage
from yukproj.settings import DEFAULT_FROM_EMAIL

def email_send(request, *args, **kwargs):
    email = EmailMessage(subject, body, DEFAULT_FROM_EMAIL, 
                         [request.user.email])
    if kwargs['msg_type'] == 'pwd_reset':
        subject = 'Password reset confirmation - Yukmarks.com'
        body = 

    email.send()