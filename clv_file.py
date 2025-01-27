#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function

import argparse
import getpass

from erppeek import *

import sqlite3
import re


def clv_file_category_export_sqlite(client, args, db_path):

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
                        file_category.name,
                        file_category.code,
                        file_category.notes
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> file_category_count: ', file_category_count)


def clv_file_category_import_sqlite(client, args, db_path):

    table_name = 'clv_file_category'

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
            id,
            parent_id,
            name,
            code,
            notes,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_file_category = client.model('clv_file.category')

    print(data)
    print([field[0] for field in cursor.description])
    file_category_count = 0
    for row in cursor:
        file_category_count += 1

        print(file_category_count, row[0], row[1], row[2], row[3], row[4])

        values = {
            'parent_id': row[1],
            'name': row[2],
            'code': row[3],
            'notes': row[4],
        }
        category_id = clv_file_category.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (category_id,
                         row[0]
                         )
                        )

    conn.commit()
    conn.close()

    print()
    print('--> file_category_count: ', file_category_count)


def clv_file_export_sqlite(client, args, db_path):

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

    conn.commit()
    conn.close()

    print()
    print('--> file_count: ', file_count)


def clv_file_import_sqlite(client, args, db_path):

    table_name = 'clv_file'
    category_table_name = 'clv_file_category'
    tag_table_name = 'clv_tag'

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
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
            image,
            new_id
        FROM ''' + table_name + ''';
    ''')

    clv_file = client.model('clv_file')

    print(data)
    print([field[0] for field in cursor.description])
    file_count = 0
    for row in cursor:
        file_count += 1

        print(file_count, row[0], row[1], row[2], row[3], '', '',
              row[6], row[7], row[8], row[9], row[10], row[11], row[12], '', row[14])

        values = {
            'name': row[1],
            'alias': row[2],
            'code': row[3],
            'description': row[4],
            'notes': row[5],
            'date_inclusion': row[6],
            'active': row[7],
            'url': row[8],
            'ct_url': row[9],
            'image': row[13]
        }
        file_id = clv_file.create(values).id

        cursor2.execute('''
                       UPDATE ''' + table_name + '''
                       SET new_id = ?
                       WHERE id = ?;''',
                        (file_id,
                         row[0]
                         )
                        )

        if row[11] != '[]':
            category_ids = row[11].split(',')
            new_category_ids = []
            for x in range(0, len(category_ids)):

                category_id = int(re.sub('[^0-9]', '', category_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + category_table_name + '''
                    WHERE id = ?;''',
                    (category_id,
                     )
                )
                new_category_id = cursor2.fetchone()[0]

                values = {
                    'category_ids': [(4, new_category_id)],
                }
                clv_file.write(file_id, values)

                new_category_ids.append(new_category_id)

            print('>>>>>', row[11], new_category_ids)

        if row[12] != '[]':

            tag_ids = row[12].split(',')
            new_tag_ids = []
            for x in range(0, len(tag_ids)):
                tag_id = int(re.sub('[^0-9]', '', tag_ids[x]))
                cursor2.execute(
                    '''
                    SELECT new_id
                    FROM ''' + tag_table_name + '''
                    WHERE id = ?;''',
                    (tag_id,
                     )
                )
                new_tag_id = cursor2.fetchone()[0]

                values = {
                    'tag_ids': [(4, new_tag_id)],
                }
                clv_file.write(file_id, values)

                new_tag_ids.append(new_tag_id)

            print('>>>>>', row[12], new_tag_ids)

    conn.commit()
    conn.close()

    print()
    print('--> file_count: ', file_count)


def clv_file_import_parent_id_sqlite(client, args, db_path):

    table_name = 'clv_file'

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    cursor2 = conn.cursor()

    data = cursor.execute('''
        SELECT
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
            image,
            new_id
        FROM ''' + table_name + '''
        WHERE parent_id != 0;
    ''')

    clv_file = client.model('clv_file')

    print(data)
    print([field[0] for field in cursor.description])
    file_count = 0
    for row in cursor:
        file_count += 1

        print(file_count, row[0], row[1], row[2], row[3], '', '',
              row[6], row[7], row[8], row[9], row[10], row[11], row[12], '', row[14])

        cursor2.execute(
            '''
            SELECT new_id
            FROM ''' + table_name + '''
            WHERE id = ?;''',
            (row[10],
             )
        )
        new_parent_id = cursor2.fetchone()[0]

        print('>>>>>', row[0], row[14], row[10], new_parent_id)

        values = {
            'parent_id': new_parent_id,
        }
        clv_file.write(row[14], values)

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

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


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
