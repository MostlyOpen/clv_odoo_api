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
import csv


def autoIncrement(start=0, step=1):
    i = start
    while 1:
        yield i
        i += step


def get_cmed_medicament_list_id(client, list_name):

    clv_cmed_medicament_list = client.model('clv_cmed_medicament.list')
    cmed_medicament_list_browse = clv_cmed_medicament_list.browse([('name', '=', list_name), ])
    cmed_medicament_list_id = cmed_medicament_list_browse.id

    if cmed_medicament_list_id == []:
        values = {
            'name': list_name,
            }
        cmed_medicament_list_id = clv_cmed_medicament_list.create(values).id
    else:
        cmed_medicament_list_id = cmed_medicament_list_id[0]

    return cmed_medicament_list_id


def clv_cmed_medicament_list_unlink(client, list_name):

    medicament_list_id = get_cmed_medicament_list_id(client, list_name)

    clv_cmed_medicament_list_item = client.model('clv_cmed_medicament.list.item')
    medicament_list_item_browse = clv_cmed_medicament_list_item.browse(
        [('list_id', '=', medicament_list_id),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item.medicament_id.name.encode('utf-8'))

        clv_cmed_medicament_list_item.unlink(medicament_list_item.id)

    clv_cmed_medicament_list = client.model('clv_cmed_medicament.list')
    medicament_list_browse = clv_cmed_medicament_list.browse(
        [('id', '=', medicament_list_id),
         ])

    for medicament_list in medicament_list_browse:
        i += 1
        print()
        print(i, medicament_list.name.encode('utf-8'))

        clv_cmed_medicament_list.unlink(medicament_list.id)

    print('--> i: ', i - 1)


def clv_cmed_medicament_unlink(client, args):

    clv_cmed_medicament = client.model('clv_cmed_medicament')
    medicament_browse = clv_cmed_medicament.browse(args)

    i = 0
    for medicament in medicament_browse:
        i += 1
        print()
        print(i, medicament.name.encode('utf-8'))

        clv_cmed_medicament.unlink(medicament.id)

    print('--> i: ', i - 1)


def clv_cmed_import_new(client, file_name, list_name, updt_medicament_data, updt_item_data):

    medicament_list_id = get_cmed_medicament_list_id(client, list_name)

    delimiter_char = ';'

    f = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)

    rownum = 0
    found = 0
    not_found = 0
    rg = False
    ct = False
    for row in r:

        if rownum == 0:
            if row[4] == 'REGISTRO':
                rg = True
            if (row[7] == 'CLASSE TERAPÊUTICA') or \
               (row[8] == 'CLASSE TERAPÊUTICA'):
                ct = True
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        PRINCIPIO_ATIVO = row[i.next()]
        CNPJ = row[i.next()]
        LABORATORIO = row[i.next()]
        CODIGO_GGREM = row[i.next()]
        if rg:
            REGISTRO = row[i.next()]
        else:
            REGISTRO = False
        EAN = row[i.next()]
        PRODUTO = row[i.next()]
        APRESENTACAO = row[i.next()]
        if ct:
            CLASSE_TERAPEUTICA = row[i.next()]
        else:
            CLASSE_TERAPEUTICA = False
        PF_0 = row[i.next()].replace(",", ".")
        if PF_0 == 'Liberado':
            PF_0 = ""
        PF_12 = row[i.next()].replace(",", ".")
        PF_17 = row[i.next()].replace(",", ".")
        PF_18 = row[i.next()].replace(",", ".")
        PF_19 = row[i.next()].replace(",", ".")
        PF_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(",", ".")
        PMC_0 = row[i.next()].replace(",", ".")
        PMC_12 = row[i.next()].replace(",", ".")
        PMC_17 = row[i.next()].replace(",", ".")
        PMC_18 = row[i.next()].replace(",", ".")
        PMC_19 = row[i.next()].replace(",", ".")
        PMC_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(",", ".")
        RESTRICAO_HOSPITALAR = row[i.next()]
        CAP = row[i.next()]
        CONFAZ_87 = row[i.next()]
        ANALISE_RECURSAL = row[i.next()]

        print(rownum, CODIGO_GGREM)

        clv_cmed_medicament = client.model('clv_cmed_medicament')
        cmed_medicament_browse = clv_cmed_medicament.browse([('codigo_ggrem', '=', CODIGO_GGREM), ])
        cmed_medicament_id = cmed_medicament_browse.id

        values = {
            'name': CODIGO_GGREM,
            'code': CODIGO_GGREM,
            'principio_ativo': PRINCIPIO_ATIVO,
            'cnpj': CNPJ,
            'latoratorio': LABORATORIO,
            'codigo_ggrem': CODIGO_GGREM,
            'registro': REGISTRO,
            'ean': EAN,
            'produto': PRODUTO,
            'apresentacao': APRESENTACAO,
            'classe_terapeutica': CLASSE_TERAPEUTICA,
            'restr_hospitalar': RESTRICAO_HOSPITALAR,
            'cap': CAP,
            'confaz_87': CONFAZ_87,
            'analise_recursal': ANALISE_RECURSAL,
            }

        if cmed_medicament_id != []:
            found += 1
            cmed_medicament_id = cmed_medicament_id[0]
            if updt_medicament_data:
                clv_cmed_medicament.write(cmed_medicament_id, values)

        else:
            not_found += 1
            cmed_medicament_id = clv_cmed_medicament.create(values)

        clv_cmed_medicament_list_item = client.model('clv_cmed_medicament.list.item')

        values = {
            'list_id': medicament_list_id,
            'medicament_id': cmed_medicament_id,
            'order': rownum,

            'pf_0': PF_0,
            'pf_12': PF_12,
            'pf_17': PF_17,
            'pf_18': PF_18,
            'pf_19': PF_19,
            'pf_17_zfm': PF_17_ZONA_FRANCA_DE_MANAUS,
            'pmc_0': PMC_0,
            'pmc_12': PMC_12,
            'pmc_17': PMC_17,
            'pmc_18': PMC_18,
            'pmc_19': PMC_19,
            'pmc_17_zfm': PMC_17_ZONA_FRANCA_DE_MANAUS,
            }
        cmed_medicament_list_item = clv_cmed_medicament_list_item.create(values)

        print('>>>>>', cmed_medicament_list_item)

        rownum += 1

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


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
    print('--> clv_cmed_medicament.py...')
    print('--> server:', server)

    get_arguments()

    from time import time
    start = time()

    client = erppeek.Client(server, dbname, username, password)

    # list_name = 'CMED_2015_08_21'
    # print('-->', client, list_name)
    # print('--> Executing clv_cmed_medicament_list_unlink()...')
    # clv_cmed_medicament_list_unlink(client, list_name)

    # medicament_args = []
    # print('-->', client, medicament_args)
    # print('--> Executing clv_cmed_medicament_unlink()...')
    # clv_cmed_medicament_unlink(client, medicament_args)

    # file_name = '/opt/openerp/cmed/CMED_2015_08_21.csv'
    # list_name = 'CMED_2015_08_21'
    # updt_medicament_data = True
    # updt_item_data = True
    # print('-->', client, file_name, list_name,
    #       updt_medicament_data, updt_item_data)
    # print('--> Executing clv_cmed_import_new()...')
    # clv_cmed_import_new(client, file_name, list_name,
    #                     updt_medicament_data, updt_item_data)

    print()
    print('--> clv_cmed_medicament.py', '- Execution time:', secondsToStr(time() - start))
    print()
