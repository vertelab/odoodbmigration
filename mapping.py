MAPS = {'res.partner': {
    'ext_id': 'idkund',
    'city': 'ort',
    'comment': 'annan_info',
    'email': 'epost',
    'name': 'namn',
    'phone': 'telefon',
    'street': 'adress',
    'vat': 'vatnr',
    'zip': 'postnr',
    'is_company': 'kundgrupp',
    'partner_ssn': 'pnrchar',
    'calc': {
        'is_company': """
vals.update({'is_company': vals['is_company'] not in ['Privat skogsägare (61)','Privatperson ej skogsägare (60)']})
"""}
}}