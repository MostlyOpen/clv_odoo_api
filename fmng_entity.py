#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
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


def fmng_entity_export_sqlite(client, args, db_path):

    table_name = 'fmng_entity'

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
            entity_code_base,
            image,
            url,
            description,
            info TEXT,
            entity_code_size,
            parent_id INTEGER,
            ct_url,
            is_album,
            create_date,
            new_id INTEGER
            );
    ''')

    fmng_entity = client.model('fmng.entity')
    fmng_entity_browse = fmng_entity.browse(args)

    fmng_entity_count = 0
    for fmng_entity_reg in fmng_entity_browse:
        fmng_entity_count += 1

        parent_id = False
        if fmng_entity_reg.parent_id is not False:
            parent_id = fmng_entity_reg.parent_id.id

        print(fmng_entity_count, fmng_entity_reg.id, parent_id, fmng_entity_reg.entity_code_base,
              fmng_entity_reg.name.encode("utf-8"))

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           alias,
                           entity_code_base,
                           image,
                           url,
                           description,
                           info,
                           entity_code_size,
                           parent_id,
                           ct_url,
                           is_album,
                           create_date
                           )
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (fmng_entity_reg.id,
                        fmng_entity_reg.name,
                        fmng_entity_reg.alias,
                        fmng_entity_reg.entity_code_base,
                        fmng_entity_reg.image,
                        fmng_entity_reg.url,
                        fmng_entity_reg.description,
                        fmng_entity_reg.info,
                        fmng_entity_reg.entity_code_size,
                        parent_id,
                        fmng_entity_reg.ct_url,
                        fmng_entity_reg.is_album,
                        str(fmng_entity_reg.create_date)
                        )
                       )

    conn.commit()
    conn.close()

    print()
    print('--> fmng_entity_count: ', fmng_entity_count)


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
    print('--> fmng_entity.py...')
    print('--> server:', server)

    get_arguments()

    from time import time
    start = time()

    client = erppeek.Client(server, dbname, username, password)

    print()
    print('--> fmng_entity.py', '- Execution time:', secondsToStr(time() - start))
    print()
