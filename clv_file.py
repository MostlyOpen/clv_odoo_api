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


def export_clv_file_category_sqlite(client, args, db_path):

    table_name = 'clv_file_category'

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
            parent_id,
            name,
            code,
            notes TEXT,
            new_id INTEGER
            );
    ''')

    clv_file_category = client.model('clv_file.category')
    file_category_browse = clv_file_category.browse(args)

    file_category_count = 0
    for file_category in file_category_browse:
        file_category_count += 1

        parent_id = False
        if file_category.parent_id is not False:
            parent_id = file_category.parent_id.id

        print(file_category_count, file_category.id, parent_id, file_category.code,
              file_category.name.encode("utf-8"), file_category.notes)

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           parent_id,
                           name,
                           code,
                           notes
                           )
                       VALUES(?,?,?,?,?)''',
                       (file_category.id,
                        parent_id,
                        file_category.code,
                        file_category.name,
                        file_category.notes
                        )
                       )

    # data = cursor.execute('''
    #     SELECT * FROM ''' + table_name + ''';
    # ''')

    # print(data)
    # print([field[0] for field in cursor.description])
    # for row in cursor:
    #     print(row)

    conn.commit()
    conn.close()

    print()
    print('--> file_category_count: ', file_category_count)


def export_clv_file_sqlite(client, args, db_path):

    table_name = 'clv_file'

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
            alias,
            code,
            description,
            notes TEXT,
            date_inclusion,
            active,
            url,
            ct_url,
            parent_id INTEGER,
            category_ids,
            tag_ids,
            image,
            new_id INTEGER
            );
    ''')

    clv_file = client.model('clv_file')
    file_browse = clv_file.browse(args)

    file_count = 0
    for file_reg in file_browse:
        file_count += 1

        parent_id = False
        if file_reg.parent_id is not False:
            parent_id = file_reg.parent_id.id

        print(file_count, file_reg.id, parent_id, file_reg.code, file_reg.name.encode("utf-8"))

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           alias,
                           code,
                           description,
                           notes,
                           date_inclusion,
                           active,
                           url,
                           ct_url,
                           parent_id,
                           category_ids,
                           tag_ids,
                           image
                           )
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (file_reg.id,
                        file_reg.name,
                        file_reg.alias,
                        file_reg.code,
                        file_reg.description,
                        file_reg.notes,
                        file_reg.date_inclusion,
                        file_reg.active,
                        file_reg.url,
                        file_reg.ct_url,
                        parent_id,
                        str(file_reg.category_ids.id),
                        str(file_reg.tag_ids.id),
                        file_reg.image
                        )
                       )

    # data = cursor.execute('''
    #     SELECT * FROM ''' + table_name + ''';
    # ''')

    # print(data)
    # print([field[0] for field in cursor.description])
    # for row in cursor:
    #     print(row)

    conn.commit()
    conn.close()

    print()
    print('--> file_count: ', file_count)


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
    print('--> clv_file.py...')
    print('--> server:', server)

    get_arguments()

    from time import time
    start = time()

    client = erppeek.Client(server, dbname, username, password)

    print()
    print('--> clv_file.py', '- Execution time:', secondsToStr(time() - start))
    print()
