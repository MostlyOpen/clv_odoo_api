#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol                 #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from __future__ import print_function

import argparse
import getpass

from erppeek import *

import sqlite3


def clv_tag_export_sqlite(client, args, db_path):

    table_name = 'clv_tag'

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY,
            name,
            code,
            notes TEXT,
            new_id INTEGER
            );
    ''')

    clv_tag = client.model('clv_tag')
    tag_browse = clv_tag.browse(args)

    tag_count = 0
    for tag in tag_browse:
        tag_count += 1

        print(tag_count, tag.id, tag.code, tag.name.encode("utf-8"), tag.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           code,
                           notes
                           )
                       VALUES(?,?,?,?)''',
                       (tag.id,
                        tag.name,
                        tag.code,
                        tag.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def clv_tag_import_sqlite(client, args, db_path):

    table_name = 'clv_tag'

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            name,
            code,
            notes,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_tag = client.model('clv_tag')

    print(data)
    print([field[0] for field in cursor.description])
    tag_count = 0
    for row in cursor:
        tag_count += 1

        print(tag_count, row[0], row[1], row[2], row[3], row[4])

        values = {
            'name': row[1],
            'code': row[2],
            'notes': row[3],
            }
        tag_id = clv_tag.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (tag_id,
                         row[0]
                         )
                        )

    conn.commit()
    conn.close()

    print()
    print('--> tag_count: ', tag_count)


def get_arguments():

    global server
    global username
    global password
    global dbname

    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action="store", dest="server")
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    args = parser.parse_args()
    print('%s%s' % ('--> ', args))

    if args.server is not None:
        server = args.server
    elif server == '*':
        server = raw_input('server: ')

    if args.dbname is not None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

    if args.username is not None:
        username = args.username
    elif username == '*':
        username = raw_input('username: ')

    if args.password is not None:
        password = args.password
    elif password == '*':
        password = getpass.getpass('password: ')


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t*1000,), 1000, 60, 60])


if __name__ == '__main__':

    server = 'http://localhost:8069'
    # server = '*'

    username = 'username'
    # username = '*'
    password = 'password'
    # password = '*'

    dbname = 'odoo'
    # dbname = '*'

    print()
    print('--> clv_tag.py...')
    print('--> server:', server)

    get_arguments()

    from time import time
    start = time()

    client = erppeek.Client(server, dbname, username, password)

    print()
    print('--> clv_tag.py', '- Execution time:', secondsToStr(time() - start))
    print()
