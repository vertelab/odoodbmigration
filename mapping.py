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
    'calc': {
        'is_company': """
vals.update({'is_company': vals['is_company'] not in ['Privatperson ej skogsägare (60)']})
"""}
}}
