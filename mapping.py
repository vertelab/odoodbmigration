MAPS = {
    # region idkund
    'idkund': {
        'model': 'res.partner',
        'calc': {
            'is_company': """
vals.update({'is_company': vals['is_company'] not in ['Privat skogsägare (61)','Privatperson ej skogsägare (60)']})
""",
            'partner_ssn': """
ssn = str(vals[key]).replace(' ','').replace('–','-').replace('_','-')
if len(ssn) == 12:
    vals['partner_ssn'] = f"{ssn[:8]}-{ssn[8:]}"
elif len(ssn) == 11 and ssn[6] == '-':
    try:
        if int(ssn[2:4])>12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn']='19'
    except (TypeError, ValueError) as e:
        print(e)
    else:
        vals['partner_ssn'] += ssn
elif len(ssn) == 10:
    try:
        if int(ssn[2:4])>12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn']='19'
    except (TypeError, ValueError) as e:
        print(e)
    else:
        vals['partner_ssn'] += f"{ssn[:6]}-{ssn[6:]}"
elif vals[key]:
    vals['partner_ssn'] = str(vals[key])
    """,
        },
        'create': {
            'city': 'ort',
            'comment': 'annan_info',
            'email': 'epost',
            'is_company': 'kundgrupp',
            'name': 'namn',
            'partner_ssn': 'pnrchar',
            'phone': 'telefon',
            'street': 'adress',
            'vat': 'vatnr',
                   'zip': 'postnr',
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
            'parent_id': """
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
if not xml_id:
    vals['category_id'] = 1
""",
        },
        'create': {
            'name': 'namn',
            'comment': 'info',
            'email': 'epost',
            'mobile': 'mobnr',
            'parent_id': 'kund.idkund',
            'phone': 'telnr',
        },
        'debug': {
            'name': 'namn',
            'comment': 'info',
            'email': 'epost',
            'mobile': 'mobnr',
            'parent_id': 'kund.idkund',
            'phone': 'telnr',
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
            'phone': """
if not str(vals[key]).startswith('0'):
    vals[key] = '0' + str(vals[key])
""",
            'mobile': """
if not str(vals[key]).startswith('0'):
    vals[key] = '0' + str(vals[key])
    """,
            'parent_id': """
xml_id = get_xml_id('idkund', vals[key])
vals[key] = get_res_id_from_xml_id(xml_id)
""",
        },
        'create': {
            # 'deltagarstatus':'deltagarstatus',
            # 'kurs':'kurs.idkurs',
            'city': 'ort',
            'email': 'epost',
            'name': 'namn',
            'phone': 'telnr',
            'street': 'adress',
            'zip': 'postnr',

            'comment': 'info',
            'email': 'epost',
            'mobile': 'mobnr',
            'parent_id': 'kund.idkund',
            'phone': 'telnr',
        },
        'debug': {
            'name': 'namn',
            'comment': 'info',
            'email': 'epost',
            'mobile': 'mobnr',
            'parent_id': 'kund.idkund',
            'phone': 'telnr',
        },
        'write': {
            'parent_id': 'kund.idkund',
        },
    },
    # endregion
}
