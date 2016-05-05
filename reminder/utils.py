from django.core.mail import send_mail
from django.template import loader



FROM_EMAIL_ADDR = 'birthdayapi@gmail.com'

def send_email(name='NAME',
        doctor_name="DOCTOR",
        subject='SUBJECT', 
        message='MESSAGE', 
        resp_addr=None, 
        to_addr='birthdayapi@gmail.com',
        contact=False, 
        birthday=False):

    if contact:
        '''for email in contact page '''
        # add suffix in message to ensure we can reply
        if name and resp_addr:
            message = message + '\n\n\n-----------\nThis message is from ' + name + ': ' + resp_addr
        elif name:
            message = message + '\n\n\n-----------\nThis message is from ' + name
        elif resp_addr:
            message = message + '\n\n\n-----------\nThis message is from email: ' + resp_addr
    elif birthday:
        '''for birthday email '''
        # In this case, message is the path of email template
        context_dict = {}
        context_dict['patient_name'] = name
        context_dict['doctor_name'] = doctor_name
        message = loader.render_to_string('email_template/birthday_email.txt', context_dict)

    '''for custom email: NO ACTION'''

    send_mail(subject, message, FROM_EMAIL_ADDR, [to_addr], fail_silently=False)






