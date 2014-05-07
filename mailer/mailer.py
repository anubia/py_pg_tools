#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import smtplib

# Definition of constants
MSG_LEVELS = {
    'info': 'INFO',
    'warn': 'WARN',
    'error': 'ERROR',
}
OP_TYPES = {
    'backup': 'Backup',
}
OP_RESULTS = {
    'ok': 'OK',
    'warn': 'Warnings, but not critical errors. Anyway, please check.',
    'error': ('There were some errors that prevented some operations. '
              'Please check immediately.'),
    'critical': ('Some critical error occurred!! Uh, uh, nothing good. '
                 'Please check immediately.'),
}
# Email full info template, for: John Doe <john.doe@email.com>
ADDR_TMPLT = '{} <{}>'
#----------------------

# Specifying the from and to addresses
from_info = {'name': 'Juanillo',
             'email': 'jfv@anubia.es'}
to_infos = [{'name': 'Juan Formoso',
             'email': 'jfv@anubia.es'},
            {'name': 'Otro email',
             'email': 'jfv@anubia.es'},
            ]
cc_infos = []
bcc_infos = [{'name': 'Juan Formoso Vasco',
              'email': 'jfv@anubia.es'},
             ]
# Sender and recipients email addresses (needed for sending the email)
from_email_str = from_info['email']
to_emails_list = [dict['email'] for dict in to_infos]
cc_emails_list = [dict['email'] for dict in cc_infos]
bcc_emails_list = [dict['email'] for dict in bcc_infos]
all_emails_list = to_emails_list + cc_emails_list + bcc_emails_list

# Sender and recipients full info (used in email message header)
from_info_str = ADDR_TMPLT.format(from_info['name'], from_info['email'])
to_infos_str = ', '.join(ADDR_TMPLT.format(dict['name'],
                                           dict['email']) for dict in to_infos)
cc_infos_str = ', '.join(ADDR_TMPLT.format(dict['name'],
                                           dict['email']) for dict in cc_infos)
# Specifying other email data (used in email message header)
mime_version = '1.0'
content_type = 'text/html'
subject = '[INFO] SMTP HTML e-mail test'

#print("from_email_str: ", from_email_str)
#print("to_emails_str: ", to_emails_str)
#print("from_info_str: ", from_info_str)
#print("to_infos_str: ", to_infos_str)

# Email header: Note Bcc info is not shown in this header
msg_header = '''From: {h_from}
To: {h_to}
Cc: {h_cc}
MIME-Version: {h_mime}
Content-type: {h_content}
Subject: {h_subject}
'''.format(h_from=from_info_str,
           h_to=to_infos_str,
           h_cc=cc_infos_str,
           h_mime=mime_version,
           h_content=content_type,
           h_subject=subject)

msg_content = '''
<h1>Sending HTML emails with Python is easy!</h1>
This is an e-mail message to be sent in HTML format.<br>
<b>This is HTML message.</b><br>
Tutorial: <a href="http://www.tutorialspoint.com/python/''' \
    '''python_sending_email.htm">http://www.tutorialspoint.com/python/''' \
    '''python_sending_email.htm</a><br>
With To, CC and BCC.<br>
<br>
¡Con eñes! ¿Y dónde hay tildes?<br>
'''

msg_full = (''.join([msg_header, msg_content])).encode()
#print(msg_full)

# Gmail Login
username = 'alejandrosantana@anubia.es'
password = ''  # My password goes here. Should not type it in clear text

#Sending the mail
try:
    # server = smtplib.SMTP('localhost')
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email_str, all_emails_list, msg_full)
    server.quit()
    print("Successfully sent email")
except smtplib.SMTPException:
    print("Error: unable to send email")
