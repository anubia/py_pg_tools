#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import smtplib  # To send emails
from email.mime.text import MIMEText  # To allow HTML texts
# To allow send alternative emails to those mail servers without HTML
from email.mime.multipart import MIMEMultipart

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from const.const import Messenger
from date_tools.date_tools import DateTools
from mail_tools.ip_address import IpAddress


class Mailer:

    level = 1  # Verbosity level of the email
    from_info = {}  # Information about the sender's email account
    to_infos = []  # List with the destiny emails
    cc_infos = []  # List with the destiny emails (carbon copy)
    bcc_infos = []  # List with the destiny emails (blind carbon copy)
    server_tag = ''  # Alias of the sender's machine
    external_ip = ''  # External IP of the sender's machine
    op_type = ''  # Executed action
    group = None  # Affected group
    bkp_path = None  # Affected path of backups
    logger = None  # Logger to show and log some messages

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
        0: ('<h2>{op_type}: <span style="color: green;">OK</span> at '
            '"{server_tag}"</h2>Date: <span style="font-weight: bold">{date}'
            '</span><br/>Time: <span style="font-weight: bold">{time}</span>'
            '<br/>Time zone: <span style="font-weight: bold">{zone}</span>'
            '<br/>Host name: <span style="font-weight: bold">{server}</span>'
            '<br/>Netifaces IPs: <span style="font-weight: bold">'
            '{internal_ips}</span><br/>External IP: <span style="font-weight: '
            'bold">{external_ip}</span><br/>Group: <span style="font-weight: '
            'bold">{group}</span><br/>Path: <span style="font-weight: bold">'
            '{bkp_path}</span><br/><br/><br/>The process has been executed '
            'succesfully.<br/><br/>You can see its log file at the following '
            'path:<br/><br/>{log_file}.'),
        1: ('<h2>{op_type}: <span style="color: orange;">WARNING</span> at '
            '"{server_tag}"</h2>Date: <span style="font-weight: bold">{date}'
            '</span><br/>Time: <span style="font-weight: bold">{time}</span>'
            '<br/>Time zone: <span style="font-weight: bold">{zone}</span>'
            '<br/>Host name: <span style="font-weight: bold">{server}</span>'
            '<br/>Netifaces IPs: <span style="font-weight: bold">'
            '{internal_ips}</span><br/>External IP: <span style="font-weight: '
            'bold">{external_ip}</span><br/>Group: <span style="font-weight: '
            'bold">{group}</span><br/>Path: <span style="font-weight: bold">'
            '{bkp_path}</span><br/><br/><br/>There were some warnings during '
            'the process, but not critical errors. Anyway, please check it, '
            'because its behaviour is not bound to have been the expected '
            'one.<br/><br/>You can see its log file at the following path:'
            '<br/><br/>{log_file}.'),
        2: ('<h2>{op_type}: <span style="color: red;">ERROR</span> at '
            '"{server_tag}"</h2>Date: <span style="font-weight: bold">{date}'
            '</span><br/>Time: <span style="font-weight: bold">{time}</span>'
            '<br/>Time zone: <span style="font-weight: bold">{zone}</span>'
            '<br/>Host name: <span style="font-weight: bold">{server}</span>'
            '<br/>Netifaces IPs: <span style="font-weight: bold">'
            '{internal_ips}</span><br/>External IP: <span style="font-weight: '
            'bold">{external_ip}</span><br/>Group: <span style="font-weight: '
            'bold">{group}</span><br/>Path: <span style="font-weight: bold">'
            '{bkp_path}</span><br/><br/><br/>There were some errors during '
            'the process, and they prevented some operations, because the '
            'execution was truncated. Please check immediately.<br/><br/>You '
            'can see its log file at the following path:<br/><br/>'
            '{log_file}.'),
        3: ('<h2>{op_type}: <span style="color: purple;">CRITICAL</span> at '
            '"{server_tag}"</h2>Date: <span style="font-weight: bold">{date}'
            '</span><br/>Time: <span style="font-weight: bold">{time}</span>'
            '<br/>Time zone: <span style="font-weight: bold">{zone}</span>'
            '<br/>Host name: <span style="font-weight: bold">{server}</span>'
            '<br/>Netifaces IPs: <span style="font-weight: bold">'
            '{internal_ips}</span><br/>External IP: <span style="font-weight: '
            'bold">{external_ip}</span><br/>Group: <span style="font-weight: '
            'bold">{group}</span><br/>Path: <span style="font-weight: bold">'
            '{bkp_path}</span><br/><br/><br/>There were some critical errors '
            'during the process. The execution could not be carried out. '
            'Please check immediately.<br/><br/>You can see its log file at '
            'the following path:<br/><br/>{log_file}.'),
    }

    OP_RESULTS_NO_HTML = {
        0: ('{op_type}: OK at "{server_tag}"\n'
            'Date: {date}\n'
            'Time: {time}\n'
            'Time zone: {zone}\n'
            'Host name: {server}\n'
            'Netifaces IPs: {internal_ips}\n'
            'External IP: {external_ip}\n'
            'Group: {group}\n'
            'Path: {bkp_path}\n'
            'The process has been executed succesfully.\n'
            'You can see its log file at the following path:\n'
            '{log_file}.\n'),
        1: ('{op_type}: WARNING at {server}\n'
            'Date: {date}\n'
            'Time: {time}\n'
            'Time zone: {zone}\n'
            'Host name: {server}\n'
            'Netifaces IPs: {internal_ips}\n'
            'External IP: {external_ip}\n'
            'Group: {group}\n'
            'Path: {bkp_path}\n'
            'There were some warnings during the process, but not critical\n'
            'errors. Anyway, please check it, because its behaviour is not\n'
            'bound to have been the expected one. You can see its\n'
            'log file at the following path: {log_file}.\n'),
        2: ('{op_type}: ERROR at {server}\n'
            'Date: {date}\n'
            'Time: {time}\n'
            'Time zone: {zone}\n'
            'Host name: {server}\n'
            'Netifaces IPs: {internal_ips}\n'
            'External IP: {external_ip}\n'
            'Group: {group}\n'
            'Path: {bkp_path}\n'
            'There were some errors during the process, and they prevented\n'
            'some operations, because the execution was truncated. Please\n'
            'check immediately. You can see its log file at the\n'
            'following path: {log_file}.\n'),
        3: ('{op_type}: CRITICAL at {server}\n'
            'Date: {date}\n'
            'Time: {time}\n'
            'Time zone: {zone}\n'
            'Host name: {server}\n'
            'Netifaces IPs: {internal_ips}\n'
            'External IP: {external_ip}\n'
            'Group: {group}\n'
            'Path: {bkp_path}\n'
            'The process has been executed succesfully.\n'
            'You can see its log file at the following path:\n'
            '{log_file}.\n'),
    }

    def __init__(self, level=1, username='', email='', password='',
                 to_infos=[], cc_infos=[], bcc_infos=[], server_tag='',
                 external_ip='', op_type='', logger=None):

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

        self.server_tag = server_tag
        self.external_ip = external_ip

    def add_group(self, group):
        '''
        Target:
            - add a group to the information sent by the email. It will be used
              in case of "Backer" being executed.
        Parameters:
            - group: the group's name.
        '''
        self.group = group

    def add_bkp_path(self, bkp_path):
        '''
        Target:
            - add a path to the information sent by the email. It will be used
              in case of "Trimmer" being executed.
        Parameters:
            - bkp_path: the path where the involved backups are stored.
        '''
        self.bkp_path = bkp_path

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
        message = Messenger.BEGINNING_MAILER
        self.logger.highlight('info', message, 'white')

        # Get current date
        date = DateTools.get_date(fmt='%d-%m-%Y')
        time = DateTools.get_date(fmt='%H:%M:%S')
        zone = DateTools.get_date(fmt='%Z')

        # Get server name and IP addresses data
        server = IpAddress.get_hostname(self.logger)

        internal_ips = ''
        netifaces = IpAddress.get_netifaces_ips(self.logger)
        if netifaces:
            last_index = len(netifaces) - 1
        for index, netiface in enumerate(netifaces):
            internal_ips += '{} > {}'.format(netiface['netiface'],
                                             netiface['ip'])
            if index != last_index:
                internal_ips += ', '

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

        # Specifying an alternative mail in case the receiver does not have a
        # mail server with HTML

        html = self.OP_RESULTS[detected_level].format(
            op_type=self.OP_TYPES[self.op_type], server_tag=self.server_tag,
            date=date, time=time, zone=zone, server=server,
            internal_ips=internal_ips, external_ip=self.external_ip,
            group=self.group, bkp_path=self.bkp_path,
            log_file=str(self.logger.log_file))

        text = self.OP_RESULTS_NO_HTML[detected_level].format(
            op_type=self.OP_TYPES[self.op_type], server_tag=self.server_tag,
            date=date, time=time, zone=zone, server=server,
            internal_ips=internal_ips, external_ip=self.external_ip,
            group=self.group, bkp_path=self.bkp_path,
            log_file=str(self.logger.log_file))

        # Specifying other email data (used in email message header)
        mail = MIMEMultipart('alternative')
        mail['From'] = from_info_str
        mail['To'] = to_infos_str
        mail['Cc'] = cc_infos_str
        mail['Subject'] = '[INFO] {op_type} results'.format(
            op_type=self.OP_TYPES[self.op_type].upper())

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container. According to RFC 2046, the last
        # part of a multipart message, in this case the HTML message, is best
        # and preferred.
        mail.attach(part1)
        mail.attach(part2)

        msg_full = mail.as_string().encode()

        if all_emails_list:

            for email in all_emails_list:
                self.logger.info(Messenger.MAIL_DESTINY.format(email=email))

            # Sending the mail
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(self.from_info['email'], self.from_info['pwd'])
                server.sendmail(from_email_str, all_emails_list, msg_full)
                server.quit()

            except smtplib.SMTPException as e:
                message = Messenger.SEND_MAIL_FAIL
                self.logger.highlight('info', message, 'yellow')
                self.logger.debug('Error en la función "send_mail": '
                                  '{}'.format(str(e)))

        else:
            message = Messenger.MAILER_HAS_NOTHING_TO_DO
            self.logger.highlight('info', message, 'yellow')

        message = Messenger.SEND_MAIL_DONE
        self.logger.highlight('info', message, 'green')
