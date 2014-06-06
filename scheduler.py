#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# To work with the crontab whose user is running the script
from crontab import CronTab

from const.const import Messenger
from logger.logger import Logger


class Scheduler:

    time = ''  # Time when the command is going to be executed in Cron
    command = ''  # Command which is going to be executed in Cron.
    logger = None  # Logger to show and log some messages

    def __init__(self, time='', command='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        self.time = time.strip()
        self.command = command.strip()

    def show_lines(self):
        '''
        Target:
            - show the lines of the program's CRON file.
        '''
        self.logger.highlight('info', Messenger.SHOWING_CRONTAB_FILE, 'white')
        print()

        cron = CronTab(user=True)

        if cron:
            for line in cron.lines:
                print(str(line))
        else:
            print('\033[1;40;93m' + Messenger.NO_CRONTAB_FILE + '\033[0m')

    def add_line(self):
        '''
        Target:
            - add a line to the program's CRON file.
        '''
        cron = CronTab(user=True)

        job = cron.new(command=self.command)

        if self.time in ['@yearly', '@annually']:
            job.setall('0 0 1 1 *')
        elif self.time == '@monthly':
            job.setall('0 0 1 * *')
        elif self.time == '@weekly':
            job.setall('0 0 * * 0')
        elif self.time in ['@daily', '@midnight']:
            job.setall('0 0 * * *')
        elif self.time == '@hourly':
            job.setall('0 * * * *')
        elif self.time == '@reboot':
            job.every_reboot()
        else:
            job.setall(self.time)

        self.logger.highlight('info', Messenger.SCHEDULER_ADDING, 'white')

        if not cron:
            self.logger.info(Messenger.CREATING_CRONTAB)

        try:
            cron.write()
            self.logger.highlight('info', Messenger.SCHEDULER_ADD_DONE,
                                  'green')
            #print(cron.render())

        except Exception as e:
            self.logger.debug('Error en la función "add_line": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.SCHEDULER_ADD_FAIL)

    def remove_line(self):
        '''
        Target:
            - remove a line from the program's CRON file.
        '''
        self.logger.highlight('info', Messenger.SCHEDULER_REMOVING, 'white')

        cron = CronTab(user=True)

        if not cron:
            self.logger.stop_exe(Messenger.NO_CRONTAB_FILE)

        deletion = False

        line = self.time + ' ' + self.command

        for job in cron:

            if str(job).strip() == line:

                try:
                    cron.remove(job)
                    message = Messenger.SCHEDULER_REMOVE_DONE.format(job=job)
                    self.logger.highlight('info', message, 'green')
                    deletion = True

                except Exception as e:
                    self.logger.debug('Error en la función "remove_line": '
                                      '{}.'.format(str(e)))
                    message = Messenger.SCHEDULER_REMOVE_FAIL.format(job=job)
                    self.logger.highlight('warning', message, 'yellow')

        if not deletion:
            self.logger.stop_exe(Messenger.NO_CRONTAB_JOB_TO_DEL)

        cron.write()
