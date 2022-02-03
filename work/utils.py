import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

from work.models import Template

server = 'smtp.mail.ru'
user = 'okidoki.service@mail.ru'
sender = 'okidoki.service@mail.ru'
password = 'DcVADNtemnDqgNqG0KYR'
recipients = ['kirillcernysev148@gmail.com']


def send_email(subject='', recipients=[], text='Новое уведомление', filepath = None):
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'OkiDoki notification <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')
    part_file = None

    if filepath:
        basename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
        part_file.set_payload(open(filepath, "rb").read())
        part_file.add_header('Content-Description', basename)
        part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
        encoders.encode_base64(part_file)

    msg.attach(part_text)
    msg.attach(part_html)
    if part_file:
        msg.attach(part_file)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()


def create_template(form, req):
    try:
        template = Template()
        data = form.cleaned_data
        data['id'] = req.user
        template.create(data)
        template.save()
        return True
    except:
        return False


def delete(signatureDoc):
    if not(signatureDoc.client):
        signatureDoc.delete()