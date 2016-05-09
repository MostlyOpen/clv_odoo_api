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
from dbfpy import dbf

import sqlite3


def autoIncrement(start=0, step=1):
    i = start
    while 1:
        yield i
        i += step


def get_abcfarma_medicament_list_id(client, list_name):

    clv_abcfarma_medicament_list = client.model('clv_abcfarma_medicament.list')
    abcfarma_medicament_list_browse = clv_abcfarma_medicament_list.browse([('name', '=', list_name), ])
    abcfarma_medicament_list_id = abcfarma_medicament_list_browse.id

    if abcfarma_medicament_list_id == []:
        values = {
            'name': list_name,
        }
        abcfarma_medicament_list_id = clv_abcfarma_medicament_list.create(values).id
    else:
        abcfarma_medicament_list_id = abcfarma_medicament_list_id[0]

    return abcfarma_medicament_list_id


def clv_abcfarma_medicament_list_unlink(client, list_name):

    medicament_list_id = get_abcfarma_medicament_list_id(client, list_name)

    clv_abcfarma_medicament_list_item = client.model('clv_abcfarma_medicament.list.item')
    medicament_list_item_browse = clv_abcfarma_medicament_list_item.browse(
        [('list_id', '=', medicament_list_id),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item.medicament_id.name.encode('utf-8'))

        clv_abcfarma_medicament_list_item.unlink(medicament_list_item.id)

    clv_abcfarma_medicament_list = client.model('clv_abcfarma_medicament.list')
    medicament_list_browse = clv_abcfarma_medicament_list.browse(
        [('id', '=', medicament_list_id),
         ])

    for medicament_list in medicament_list_browse:
        i += 1
        print()
        print(i, medicament_list.name.encode('utf-8'))

        clv_abcfarma_medicament_list.unlink(medicament_list.id)

    print('--> i: ', i - 1)


def clv_abcfarma_medicament_unlink(client, args):

    clv_abcfarma_medicament = client.model('clv_abcfarma_medicament')
    medicament_browse = clv_abcfarma_medicament.browse(args)

    i = 0
    for medicament in medicament_browse:
        i += 1
        print()
        print(i, medicament.name.encode('utf-8'))

        clv_abcfarma_medicament.unlink(medicament.id)

    print('--> i: ', i - 1)


def clv_abcfarma_medicament_import(client, file_name, list_name, updt_medicament_data, updt_item_data):

    medicament_list_id = get_abcfarma_medicament_list_id(client, list_name)

    db = dbf.Dbf(file_name)

    names = []
    for field in db.header.fields:
        names.append(field.name)
    print(names)

    rownum = 0
    found = 0
    not_found = 0
    for rec in db:

        if rownum == 0:
            rownum += 1

        row = rec.fieldData

        i = autoIncrement(0, 1)

        MED_ABC = row[i.next()]
        MED_CTR = row[i.next()]
        MED_LAB = row[i.next()]
        LAB_NOM = row[i.next()]
        MED_DES = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_APR = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_PCO18 = row[i.next()]
        MED_PLA18 = row[i.next()]
        MED_FRA18 = row[i.next()]
        MED_PCO17 = row[i.next()]
        MED_PLA17 = row[i.next()]
        MED_FRA17 = row[i.next()]
        MED_PCO12 = row[i.next()]
        MED_PLA12 = row[i.next()]
        MED_FRA12 = row[i.next()]
        MED_UNI = row[i.next()]
        MED_IPI = row[i.next()]
        MED_DTVIG = row[i.next()]
        EXP_13 = row[i.next()]
        MED_BARRA = row[i.next()]
        MED_GENE = row[i.next()]
        MED_NEGPOS = row[i.next()]
        MED_PRINCI = row[i.next()]
        MED_PCO19 = row[i.next()]
        MED_PLA19 = row[i.next()]
        MED_FRA19 = row[i.next()]
        MED_PCOZFM = row[i.next()]
        MED_PLAZFM = row[i.next()]
        MED_FRAZFM = row[i.next()]
        MED_PCO0 = row[i.next()]
        MED_PLA0 = row[i.next()]
        MED_FRA0 = row[i.next()]
        MED_REGIMS = row[i.next()]
        MED_VARPRE = row[i.next()]

        print(rownum, MED_ABC, MED_DES, MED_APR)

        clv_abcfarma_medicament = client.model('clv_abcfarma_medicament')
        abcfarma_medicament_browse = clv_abcfarma_medicament.browse([('med_abc', '=', MED_ABC), ])
        abcfarma_medicament_id = abcfarma_medicament_browse.id

        values = {
            'name': '/',
            'code': MED_ABC,
            'med_abc': MED_ABC,
            'med_ctr': MED_CTR,
            'med_lab': MED_LAB,
            'lab_nom': LAB_NOM,
            'med_des': MED_DES,
            'med_apr': MED_APR,
            'med_barra': str(MED_BARRA),
            'med_negpos': MED_NEGPOS,
            'med_gene': MED_GENE,
            'med_princi': MED_PRINCI,
        }

        if abcfarma_medicament_id != []:
            found += 1
            abcfarma_medicament_id = abcfarma_medicament_id[0]
            if updt_medicament_data:
                clv_abcfarma_medicament.write(abcfarma_medicament_id, values)

        else:
            not_found += 1
            abcfarma_medicament_id = clv_abcfarma_medicament.create(values)

        clv_abcfarma_medicament_list_item = client.model('clv_abcfarma_medicament.list.item')

        values = {
            'list_id': medicament_list_id,
            'medicament_id': abcfarma_medicament_id,
            'order': rownum,

            'med_pco18': MED_PCO18,
            'med_pla18': MED_PLA18,
            'med_fra18': MED_FRA18,
            'med_pco17': MED_PCO17,
            'med_pla17': MED_PLA17,
            'med_fra17': MED_FRA17,
            'med_pco12': MED_PCO12,
            'med_pla12': MED_PLA12,
            'med_fra12': MED_FRA12,
            'med_pco19': MED_PCO19,
            'med_pla19': MED_PLA19,
            'med_fra19': MED_FRA19,
            'med_pcozfm': MED_PCOZFM,
            'med_plazfm': MED_PLAZFM,
            'med_frazfm': MED_FRAZFM,
            'med_pco0': MED_PCO0,
            'med_pla0': MED_PLA0,
            'med_fra0': MED_FRA0,

            'med_uni': MED_UNI,
            'med_ipi': MED_IPI,
            'med_dtvig': str(MED_DTVIG),
            'exp_13': EXP_13,
            'med_regims': MED_REGIMS,
            'med_varpre': MED_VARPRE,
        }
        abcfarma_medicament_list_item = clv_abcfarma_medicament_list_item.create(values)

        print('>>>>>', abcfarma_medicament_list_item.id)

        rownum += 1

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_abcfarma_medicament_export_sqlite(client, args, db_path):

    table_name = 'clv_abcfarma_medicament'

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
            ean13,
            code,
            medicament_name,
            concentration,
            presentation,
            pres_form,
            pres_quantity,
            pres_quantity_unit,
            notes TEXT,
            date_inclusion,
            active,
            is_product,
            is_fraction,
            for_hospital_use,
            active_component INTEGER,
            manufacturer INTEGER,

            med_abc,
            med_ctr,
            med_lab,
            lab_nom,
            med_des,
            med_apr,
            med_barra,
            med_gene,
            med_negpos,
            med_princi,
            new_id INTEGER
            );
    ''')

    clv_abcfarma_medicament = client.model('clv_abcfarma_medicament')
    file_browse = clv_abcfarma_medicament.browse(args)

    file_count = 0
    for abcfarma_medicament_reg in file_browse:
        file_count += 1

        print(file_count, abcfarma_medicament_reg.id, abcfarma_medicament_reg.code,
              abcfarma_medicament_reg.name.encode("utf-8"))

        pres_form = False
        if abcfarma_medicament_reg.pres_form:
            pres_form = abcfarma_medicament_reg.pres_form.id

        pres_quantity_unit = False
        if abcfarma_medicament_reg.pres_quantity_unit:
            pres_quantity_unit = abcfarma_medicament_reg.pres_quantity_unit.id

        active_component = False
        if abcfarma_medicament_reg.active_component:
            active_component = abcfarma_medicament_reg.active_component.id

        manufacturer = False
        if abcfarma_medicament_reg.manufacturer:
            manufacturer = abcfarma_medicament_reg.manufacturer.id

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           id,
                           name,
                           ean13,
                           code,
                           medicament_name,
                           concentration,
                           presentation,
                           pres_form,
                           pres_quantity,
                           pres_quantity_unit,
                           notes,
                           date_inclusion,
                           active,
                           is_product,
                           is_fraction,
                           for_hospital_use,
                           active_component,
                           manufacturer,

                           med_abc,
                           med_ctr,
                           med_lab,
                           lab_nom,
                           med_des,
                           med_apr,
                           med_barra,
                           med_gene,
                           med_negpos,
                           med_princi
                           )
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (abcfarma_medicament_reg.id,
                        abcfarma_medicament_reg.name,
                        abcfarma_medicament_reg.ean13,
                        abcfarma_medicament_reg.code,
                        abcfarma_medicament_reg.medicament_name,
                        abcfarma_medicament_reg.concentration,
                        abcfarma_medicament_reg.presentation,
                        pres_form,
                        abcfarma_medicament_reg.pres_quantity,
                        pres_quantity_unit,
                        abcfarma_medicament_reg.notes,
                        abcfarma_medicament_reg.date_inclusion,
                        abcfarma_medicament_reg.active,
                        abcfarma_medicament_reg.is_product,
                        abcfarma_medicament_reg.is_fraction,
                        abcfarma_medicament_reg.for_hospital_use,
                        active_component,
                        manufacturer,

                        abcfarma_medicament_reg.med_abc,
                        abcfarma_medicament_reg.med_ctr,
                        abcfarma_medicament_reg.med_lab,
                        abcfarma_medicament_reg.lab_nom,
                        abcfarma_medicament_reg.med_des,
                        abcfarma_medicament_reg.med_apr,
                        abcfarma_medicament_reg.med_barra,
                        abcfarma_medicament_reg.med_gene,
                        abcfarma_medicament_reg.med_negpos,
                        abcfarma_medicament_reg.med_princi,
                        )
                       )

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
    print('--> clv_abcfarma_medicament.py...')
    print('--> server:', server)

    get_arguments()

    from time import time
    start = time()

    client = erppeek.Client(server, dbname, username, password)

    print()
    print('--> clv_abcfarma_medicament.py', '- Execution time:', secondsToStr(time() - start))
    print()
