#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import smtplib  # To send emails

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from const.const import Messenger


class Mailer:

    level = 1
    from_info = {}
    to_infos = []
    cc_infos = []
    bcc_infos = []
    op_type = ''
    logger = None

    # Definition of constants
    OP_TYPES = {
        'u': 'Undefined method',
        'a': 'Alterer',
        'B': 'Backer',
        'd': 'Dropper',
        'r': 'Replicator',
        'R': 'Restorer',
        'T': 'Trimmer',
        't': 'Terminator',
        'v': 'Vacuumer',
    }
    OP_RESULTS = {
        0: ('<h1>{op_type} > <font color="green">OK</font></h1>\n'
            'The process has been executed succesfully.<br/><br/>You can see\n'
            'its log file at the following path:<br/><br/>\n'
            '<b>{log_file}</b>.\n'),
        1: ('<h1>{op_type} > <font color="orange">WARNING</font></h1>\n'
            'There were some warnings during the process, but not critical\n'
            'errors. Anyway, please check it, because its behaviour is not\n'
            'bound to have been the expected one.<br/><br/>You can see its\n'
            'log file at the following path:<br/><br/><b>{log_file}</b>.\n'),
        2: ('<h1>{op_type} > <font color="red">ERROR</font></h1>\n'
            'There were some errors during the process, and they prevented\n'
            'some operations, because the execution was truncated. Please\n'
            'check immediately.<br/><br/>You can see its log file at the\n'
            'following path:<br/><br/><b>{log_file}</b>.\n'),
        3: ('<h1>{op_type} > <font color="purple">CRITICAL</font></h1>\n'
            'There were some critical errors during the process. The\n'
            'execution could not be carried out. Please check immediately.\n'
            '<br/><br/>You can see its log file at the following path:\n'
            '<br/><br/><b>{log_file}</b>.\n'),
    }

    def __init__(self, level=1, username='', email='', password='',
                 to_infos=[], cc_infos=[], bcc_infos=[], op_type='',
                 logger=None):

        if logger:
            self.logger = logger
        else:
            from logger.logger import Logger
            self.logger = Logger()

        if isinstance(level, int) and level in Default.MAIL_LEVELS:
            self.level = level
        elif Checker.str_is_int(level):
            self.level = Casting.str_to_int(level)
        else:
            self.level = Default.MAIL_LEVEL

        self.from_info['email'] = email
        if not Checker.str_is_valid_mail(email):
            message = Messenger.INVALID_FROM_MAIL.format(
                email=email)
            self.logger.highlight('warning', message, 'yellow')

        self.from_info['name'] = username
        if username is '':
            message = Messenger.INVALID_FROM_USERNAME
            self.logger.highlight('warning', message, 'yellow')

        self.from_info['pwd'] = password
        if password is '':
            message = Messenger.INVALID_FROM_PASSWORD
            self.logger.highlight('warning', message, 'yellow')

        to_infos = Casting.str_to_list(to_infos)
        self.to_infos = self.get_mail_infos(to_infos)

        cc_infos = Casting.str_to_list(cc_infos)
        self.cc_infos = self.get_mail_infos(cc_infos)

        bcc_infos = Casting.str_to_list(bcc_infos)
        self.bcc_infos = self.get_mail_infos(bcc_infos)

        if op_type in self.OP_TYPES.keys():
            self.op_type = op_type
        else:
            self.op_type = 'u'

    def get_mail_infos(self, mail_infos):
        '''
        Target:
            - takes a list of strings with mail data and a "username <email>"
              format, splits it into parts and gives the same data stored and
              classified in a dictionary.
        Parameters:
            - mail_infos: the list of strings to be converted.
        Return:
            - a list of dictionaries with the username and the address of some
              mail accounts.
        '''
        temp_list = []

        for record in mail_infos:

            if Checker.str_is_valid_mail_info(record):

                mail_info = Casting.str_to_mail_info(record)

                if Checker.str_is_valid_mail(mail_info['email']):
                    temp_list.append(mail_info)
                else:
                    message = Messenger.INVALID_TO_MAIL.format(
                        email=mail_info['email'])
                    self.logger.highlight('warning', message, 'yellow')

            else:
                message = Messenger.INVALID_TO_MAIL_INFO.format(
                    mail_info=record)
                self.logger.highlight('warning', message, 'yellow')

        return temp_list

    def send_mail(self, detected_level):
        '''
        Target:
            - send an email to the specified email addresses.
        '''

        # Email full info template, for: John Doe <john.doe@email.com>
        ADDR_TMPLT = '{} <{}>'

        # Sender and recipients email addresses (needed for sending the email)
        from_email_str = self.from_info['email']
        to_emails_list = [dict['email'] for dict in self.to_infos]
        cc_emails_list = [dict['email'] for dict in self.cc_infos]
        bcc_emails_list = [dict['email'] for dict in self.bcc_infos]
        all_emails_list = to_emails_list + cc_emails_list + bcc_emails_list

        # Sender and recipients full info (used in email message header)
        from_info_str = ADDR_TMPLT.format(self.from_info['name'],
                                          self.from_info['email'])
        to_infos_str = ', '.join(ADDR_TMPLT.format(
            dict['name'], dict['email']) for dict in self.to_infos)
        cc_infos_str = ', '.join(ADDR_TMPLT.format(
            dict['name'], dict['email']) for dict in self.cc_infos)

        # Specifying other email data (used in email message header)
        mime_version = '1.0'
        content_type = 'text/html'
        subject = '[INFO] {op_type} results'.format(
            op_type=self.OP_TYPES[self.op_type].upper())

        # Email header: Note Bcc info is not shown in this header
        msg_header = Messenger.MAIL_HEADER.format(
            h_from=from_info_str, h_to=to_infos_str, h_cc=cc_infos_str,
            h_mime=mime_version, h_content=content_type, h_subject=subject)

        #msg_content = Messenger.MAIL_CONTENT
        msg_content = self.OP_RESULTS[detected_level].format(
            op_type=self.OP_TYPES[self.op_type],
            log_file=str(self.logger.log_file))

        msg_full = (''.join([msg_header, msg_content])).encode()

        message = Messenger.BEGINNING_MAILER
        self.logger.highlight('info', message, 'white')

        if all_emails_list:

            self.logger.info(Messenger.MAIL_DESTINATARIES.format(
                emails=all_emails_list))

            # Sending the mail
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(self.from_info['email'], self.from_info['pwd'])
                server.sendmail(from_email_str, all_emails_list, msg_full)
                server.quit()

            except smtplib.SMTPException:
                message = Messenger.SEND_MAIL_FAIL
                self.logger.highlight('info', message, 'yellow')

        else:
            message = Messenger.MAILER_HAS_NOTHING_TO_DO
            self.logger.highlight('info', message, 'yellow')

        message = Messenger.SEND_MAIL_DONE
        self.logger.highlight('info', message, 'green')
