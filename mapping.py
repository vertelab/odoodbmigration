MAPS = {
    # region idkund
    'idkund': {
        'model': 'res.partner',
        'calc': {
            'email': """
if not vals[key]:
    vals[key] = ''
""",
            'name': """
if type(vals[key]) is int:
    vals[key] = str(vals[key])
""",
            'partner_ssn': """
vals['category_id'] = [(4, 3, 0)]
if not vals[key]:
    vals[key] = False
else:
    ssn = str(vals[key]).replace(' ', '').replace('–', '-').replace('_', '-')
    if len(ssn) == 12:
        vals['partner_ssn'] = f"{ssn[:8]}-{ssn[8:]}"
        if int(ssn[4:6]) > 12:
            vals['is_company'] = True
        else:
            vals['is_company'] = False
    elif len(ssn) == 11 and ssn[6] == '-':
        if int(ssn[2:4]) > 12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn'] = '19'
            vals['is_company'] = False
        vals['partner_ssn'] += ssn
    elif len(ssn) == 10:
        if int(ssn[2:4]) > 12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn'] = '19'
            vals['is_company'] = False
        vals['partner_ssn'] += f"{ssn[:6]}-{ssn[6:]}"
""",
        },
        'create': {
            'vat': 'vatnr',
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telefon',
            'street': 'adress',
            'comment': 'annan_info',
            'partner_ssn': 'pnrchar',
        },
        'debug': {
            'email': 'epost',
        },
        'write': {
            'email': 'epost',
        },
    },
    # endregion
    # region idpepers
    'idpepers': {
        'model': 'res.partner',
        'calc': {
            'email': """
if not vals[key]:
    vals[key] = ''
""",
            'mobile': """
if type(vals[key]) is int:
    if not str(vals[key]).startswith('0'):
        vals[key] = '0' + str(vals[key])
""",
            'name': """
if type(vals[key]) is int:
    vals[key] = str(vals[key])
""",
            'parent_id': """
vals['category_id'] = [(4, 4, 0)]
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
if not vals[key]:
    vals[key] = False
    vals['category_id'].append((4, 1, 0))
""",
            'phone': """
if type(vals[key]) is int:
    if not str(vals[key]).startswith('0'):
        vals[key] = '0' + str(vals[key])
""",
        },
        'create': {
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'mobile': 'mobnr',
            'comment': 'info',
            'parent_id': 'kund.idkund',
        },
        'debug': {
            'email': 'epost',
        },
        'write': {
            'email': 'epost',
        },
    },
    # endregion
    # region idkursdeltagare
    'idkursdeltagare': {
        'model': 'res.partner',
        'calc': {
            'name': """
if type(vals[key]) is int:
    vals[key] = str(vals[key])
""",
            'parent_id': """
vals['category_id'] = [(4, 5, 0)]
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
if not vals[key]:
    vals[key] = False
    vals['category_id'].append((4, 1, 0))
""",
            'phone': """
if type(vals[key]) is int:
    if not str(vals[key]).startswith('0'):
        vals[key] = '0' + str(vals[key])
""",
        },
        'create': {
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'street': 'adress',
            'parent_id': 'kund.idkund',
        },
        'debug': {
            'parent_id': 'kund.idkund',
        },
        'write': {
            'parent_id': 'kund.idkund',
        },
    },
    # endregion
    # region fafast.xlsx
    'idfafast': {
        'model': 'property.property',
        'calc': {
            'name': """
if type(vals[key]) is int:
    vals[key] = str(vals[key])
""",
        },
        'create': {
            'name': 'namnfast',
            'property_key': 'fastnr',
        },
        'debug': {
            'name': 'namnfast',
            'property_key': 'fastnr',
        },
        'write': {
            'name': 'namnfast',
            'property_key': 'fastnr',
        },
    },
    # endregion
    # region fafast.xlsx 9
    'agare_idagare': {
        'model': 'property.stakeholder',
        'calc': {
            'partner_id': """
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
if not vals[key]:
    vals['skip'] = True
""",
            'property_id': """
xml_id = get_xml_id('idfafast', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
""",
        },
        'create': {
            'partner_id': 'agare.idagare',
            'property_id': 'idfafast',
        },
        'debug': {
            'partner_id': 'agare.idagare',
            'property_id': 'idfafast',
        },
        'write': {
            'partner_id': 'agare.idagare',
            'property_id': 'idfafast',
        },
    },
    # endregion
    # region kurs.xlsx
    'idkurs': {
        'model': 'event.event',
        'calc': {
            'date_begin': """
if not vals['date_begin']:
    vals['skip'] = True
else:
    date_begin_time = vals.pop('date_begin_time')
    if not date_begin_time:
        date_begin_time = '00:00'
    fmt = '%Y-%m-%d %H:%M'
    tz = pytz.timezone('Europe/Stockholm')
    naive = datetime.strptime(f"{vals[key]} {date_begin_time}", fmt)
    local = tz.localize(naive, is_dst=True)
    date_begin = local.astimezone(pytz.utc)
    vals['date_begin'] = datetime.strftime(date_begin, fmt)
    if vals['date_end']:
        date_end = date_begin + timedelta(days=vals['date_end'])
        vals['date_end'] = datetime.strftime(date_end, fmt)
    else:
        vals['date_end'] = vals['date_begin']
""",
        },
        'create': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
        },
        'debug': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
        },
        'write': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
        },
    },
    # endregion
}
