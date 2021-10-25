MAPS = {
    'res.partner': {
        'calc': {
            'is_company': """
vals.update({'is_company': vals['is_company'] not in [
            'Privat skogsägare (61)','Privatperson ej skogsägare (60)']})
            """,
            'partner_ssn': """
ssn = str(vals[key]).replace(' ','').replace('–','-').replace('_','-')
if len(ssn) == 12 and ssn.startswith('19') or ssn.startswith('SE'):
    vals.update({'partner_ssn': f"{ssn[2:8]}-{ssn[8:]}"})
elif len(ssn) == 11 and ssn[6] == '-':
    vals.update({'partner_ssn': ssn})
elif len(ssn) == 10:
    vals.update({'partner_ssn': f"{ssn[:6]}-{ssn[6:]}"})
else:
    vals.update({'partner_ssn': str(vals[key])})
    print(vals['ext_id'], vals[key])
            """,
        },
        'create': {
            'ext_id': 'idkund',
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
            'ext_id': 'idkund',
            'partner_ssn': 'pnrchar',
        },
        'write': {
            'ext_id': 'idkund',
            'partner_ssn': 'pnrchar',
        },
    },
}
