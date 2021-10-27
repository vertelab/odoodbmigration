MAPS = {
    # region idkund
    'idkund': {
        'model': 'res.partner',
        'calc': {
            'name': """
if type(vals[key]) == int:
    vals[key] = str(vals[key])
vals['break'] = False
""",
            'partner_ssn': """
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
vals['category_id'] = [(4, 3, 0)]
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
            'partner_ssn': 'pnrchar',
        },
        'write': {
            'partner_ssn': 'pnrchar',
        },
    },
    # endregion
    # region idpepers
    'idpepers': {
        'model': 'res.partner',
        'calc': {
            'phone': """
if not str(vals[key]).startswith('0'):
    vals[key] = '0' + str(vals[key])
    """,
            'mobile': """
if not str(vals[key]).startswith('0'):
    vals[key] = '0' + str(vals[key])
    """,
            'name': """
if type(vals[key]) == int:
    vals[key] = str(vals[key])
vals['break'] = False
""",
            'parent_id': """
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
vals['category_id'] = [(4, 4, 0)]
if not xml_id:
    vals['category_id'].append((4, 1, 0))
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
            'parent_id': 'kund.idkund',
        },
        'write': {
            'parent_id': 'kund.idkund',
        },
    },
    # endregion
    # region idkursdeltagare
    'idkursdeltagare': {
        'model': 'res.partner',
        'calc': {
            'name': """
if type(vals[key]) == int:
    vals[key] = str(vals[key])
""",
            'parent_id': """
vals['break'] = False
vals['category_id'] = [(4, 5, 0)]
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
""",
            'phone': """
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
vals['break'] = False
""",
        },
        'create': {
            'name': 'namnfast',
        },
        'debug': {
            'name': 'namnfast',
        },
        'write': {
            'name': 'namnfast',
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
if type(vals[key]) is int:
    vals['break'] = False
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
}
