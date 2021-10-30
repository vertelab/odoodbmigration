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
        'fields': {
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
xmlid = get_xmlid('idkund', vals[key])
vals[key] = get_res_id_from_xmlid(xmlid)
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
        'fields': {
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'mobile': 'mobnr',
            'comment': 'info',
            'parent_id': 'kund.idkund',
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
xmlid = get_xmlid('idkund', vals[key])
vals[key] = get_res_id_from_xmlid(xmlid)
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
        'fields': {
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'street': 'adress',
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
        'fields': {
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
xmlid = get_xmlid('idkund', vals[key])
vals[key] = get_res_id_from_xmlid(xmlid)
if not vals[key]:
    vals['skip'] = True
""",
            'property_id': """
xmlid = get_xmlid('idfafast', vals[key])
vals[key] = get_res_id_from_xmlid(xmlid)
""",
        },
        'fields': {
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
        'fields': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
        },
    },
    # endregion
    # region artikel.xlsx
    'idartikel': {
        'model': 'product.template',
        'fields': {
            'name': 'benamning',
            'list_price': 'pris',
            'sale_order_template_id': 'produkt.idprodukt',
            'uom_id': 'enhet',
        },
        'pre_sync': """
vals['list_price'] = float(vals['list_price'].split(',')[0].replace('.',''))

UOM = {
    'dag': 'day', 
    'ha': 'ha',
    'km': 'km',
    'm3': 'cubic_meter', 
    'tim': 'hour',
    }

uom = vals['uom_id']
uom_xmlid = f"uom.product_uom_{UOM.get(uom, 'unit')}"

vals['uom_id'] = get_res_id_from_xmlid(uom_xmlid)

if not vals['uom_id'] and uom == 'ha':
    area_id = get_res_id_from_xmlid('uom.uom_categ_area')
    if not area_id:
        area_id = target.env['uom.category'].create({'name':'Area'})
        area_xmlid = {
            'model': 'uom.category',
            'module': 'uom',
            'name': 'uom_categ_area',
            'res_id': area_id,
            }
        target.env['ir.model.data'].create(area_xmlid)
        
    m2_id = get_res_id_from_xmlid('uom.product_uom_square_meter')
    if not m2_id:
        m2_id = target.env['uom.uom'].create({
            'category_id': area_id,
            'name': 'm²',
            })
        target.env['ir.model.data'].create({
            'model': 'uom.uom',
            'module': 'uom',
            'name': 'product_uom_square_meter',
            'res_id': m2_id,
            })
            
    ha_id = target.env['uom.uom'].create({
        'category_id': area_id,
        'factor': 0.0001,
        'name': 'ha',
        'uom_type':'bigger',
        })               

    target.env['ir.model.data'].create({
        'model': 'uom.uom',
        'module': 'uom',
        'name': 'product_uom_ha',
        'res_id': ha_id,
        })
    vals['uom_id'] = ha_id

vals['uom_po_id'] = vals['uom_id']
sot_xmlid = get_xmlid('idprod_reg', vals.pop('sale_order_template_id'))
maps['sot_xmlid'] = sot_xmlid
""",
        'post_sync': """
template_id = get_res_id_from_xmlid(xmlid)
if template_id:
    template = target.env['product.template'].read(template_id)[0]
    product_id = template['product_variant_id'][0]
    if product_id:
        so_template_id = get_res_id_from_xmlid(maps.get('sot_xmlid'))
        if so_template_id:
            sotl_ext_model = 'artikel'
            sotl_xmlid = get_xmlid(sotl_ext_model, xmlid.split('_')[-1])
            sotl_model = 'sale.order.template.line'
            sotl_vals = {
                'name': template['name'],
                'product_id': product_id,
                'product_uom_id': vals['uom_id'],
                'sale_order_template_id': so_template_id,
                }
            if mode == 'debug':
                print(f"{sotl_vals=}")
            else:
                if not create_record_and_xmlid(sotl_model, sotl_vals, sotl_xmlid):
                    write_record(sotl_model, sotl_vals, sotl_xmlid)
"""
    },
    # endregion
    # region prod_reg.xlsx
    'idprod_reg': {
        'model': 'sale.order.template',
        'calc': {
        },
        'fields': {
            'name': 'namn',
            'note': 'beskrivning',
        },
    },
    # endregion
}
