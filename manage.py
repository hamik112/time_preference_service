from flask import Flask, render_template, redirect, jsonify, current_app, request, session, g, abort, Blueprint, render_template_string
from flask_script import Manager, Command
from main import application, redis
import csv
# configure your app
manager = Manager(application)


class UpdateUserPreferenceFromCsv(Command):
    """
    Updates user preference from csv
    """

    def run(self):
        with open('data/db/user_preference_data.csv', 'rb') as csv_file:
            l = csv.reader(csv_file, delimiter=',')
            i = 0
            for row in l:

                i = 1
        return 


class FlushRedis(Command):
    """
    Flush Redis
    """

    def run(self):
        redis.flushall()
        return


manager.add_command('update_user_preference', UpdateUserPreferenceFromCsv())
manager.add_command('flush_redis', FlushRedis())
if __name__ == "__main__":
    manager.run()

