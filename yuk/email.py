from django.core.mail import EmailMessage
from yukproj.settings import DEFAULT_FROM_EMAIL

def item_saved(sender, **kwargs):
    subject="foo"
    body="bar"
    email = EmailMessage(subject, body, DEFAULT_FROM_EMAIL, 
                         ['matt.deboard@gmail.com'])
    email.send()