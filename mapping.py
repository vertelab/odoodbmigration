MAPS = {
    # region kund.xlsx
    'idkund': {
        'model': 'res.partner',
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
        'pre_sync': """
vals['category_id'] = [(4, 3, 0)]

if not vals['email']:
    vals['email'] = ''
    
if not vals['phone']:
    vals['phone'] = ''
    
if not vals['vat']:
    vals['vat'] = ''
else:
    vals['vat'] = str(vals['vat'])
    
if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

if not vals['partner_ssn']:
    vals['partner_ssn'] = False
else:
    ssn = str(vals['partner_ssn']).replace(' ', '').replace('–', '-').replace('_', '-')
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
    # endregion
    # region pepers.xlsx
    'idpepers': {
        'model': 'res.partner',
        'fields': {
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'mobile': 'mobnr',
            'comment': 'info',
            'parent_id': 'kund.idkund',
        },
        'pre_sync': """
vals['category_id'] = [(4, 4, 0)]
            
if not vals['email']:
    vals['email'] = ''

if type(vals['mobile']) is int:
    if not str(vals['mobile']).startswith('0'):
        vals['mobile'] = '0' + str(vals['mobile'])

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

parent_xmlid = get_xmlid('idkund', vals['parent_id'])
vals['parent_id'] = get_res_id_from_xmlid(parent_xmlid)
if not vals['parent_id']:
    vals['parent_id'] = False
    vals['category_id'].append((4, 1, 0))
            
if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])
""",
    },
    # endregion
    # region kursdeltagare.xlsx
    'idkursdeltagare': {
        'model': 'res.partner',
        'fields': {
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'street': 'adress',
            'parent_id': 'kund.idkund',
        },
        'pre_sync': """
vals['category_id'] = [(4, 5, 0)]

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])
    
parent_xmlid = get_xmlid('idkund', vals['parent_id'])
vals['parent_id'] = get_res_id_from_xmlid(parent_xmlid)
if not vals['parent_id']:
    vals['parent_id'] = False
    vals['category_id'].append((4, 1, 0))

if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])
""",
    },
    # endregion
    # region fafast.xlsx
    'idfafast': {
        'model': 'property.property',
        'fields': {
            'name': 'namnfast',
            'property_key': 'fastnr',
        },
        'pre_sync': """
if type(vals['name']) is int:
    vals['name'] = str(vals['name'])
""",
    },
    # endregion
    # region fafast.xlsx 9
    'agare_idagare': {
        'model': 'property.stakeholder',
        'fields': {
            'partner_id': 'agare.idagare',
            'property_id': 'idfafast',
        },
        'pre_sync': """
partner_xmlid = get_xmlid('idkund', vals['partner_id'])
vals['partner_id'] = get_res_id_from_xmlid(partner_xmlid)
if not vals['partner_id']:
    vals['skip'] = True

property_xmlid = get_xmlid('idfafast', vals['property_id'])
vals['property_id'] = get_res_id_from_xmlid(property_xmlid)
""",
    },
    # endregion
    # region kurs.xlsx
    'idkurs': {
        'model': 'event.event',
        'fields': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
            'user_id': 'kursansvarig.anvandare',
        },
        'pre_sync': """
if not vals['date_begin']:
    vals['skip'] = True
else:
    if vals['user_id']:
        user_id = target.env['res.users'].search([
            ('login', '=', vals['user_id']),
            ])
        if user_id:
            vals['user_id'] = user_id[0]
    if not vals['user_id']:
        vals.pop('user_id')
    date_begin_time = vals.pop('date_begin_time')
    if not date_begin_time:
        date_begin_time = '00:00'
    fmt = '%Y-%m-%d %H:%M'
    tz = pytz.timezone('Europe/Stockholm')
    naive = datetime.strptime(f"{vals['date_begin']} {date_begin_time}", fmt)
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

### Create in a datafile instead
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
        'fields': {
            'name': 'namn',
            'note': 'beskrivning',
        },
        'pre_sync': {
        },
    },
    # endregion
    # region uppdrag.xlsx
    'iduppdrag': {
        'model': 'sale.order',
        'fields': {
            'summa': 'summa_fakturerat',
            'note':'annan_info',
            'partner_id': 'markning',
            'projekt': 'projekt',
            'projektnamn': 'uppdragsbenamning',
            },
        'pre_sync': """
partner_xmlid = get_xmlid('idkund', vals['partner_id'])
vals['partner_id'] = get_res_id_from_xmlid(partner_xmlid)
if not vals['partner_id']:
    vals['skip'] = True

maps['projekt'] = vals.pop('projekt')
maps['projektnamn'] = vals.pop('projektnamn')
maps['summa'] = vals.pop('summa')
""",
        'post_sync': """
order_id = get_res_id_from_xmlid(xmlid)
product_xmlid = get_xmlid('slask', 'produkt')
product_id = get_res_id_from_xmlid(product_xmlid)
price_unit = 0
if maps['summa']:
    price_unit = float(maps['summa'].split(',')[0].replace('.',''))

if not product_id:
    template_xmlid = get_xmlid('slask', 'produktmall')
    template_id = get_res_id_from_xmlid(template_xmlid)
    if not template_id:
        template_id = create_record_and_xmlid('product.template', {'name': 'Migreringsprodukt'}, template_xmlid)

    template = target.env['product.template'].read(template_id)[0]
    product_id = template['product_variant_id'][0]
    create_xmlid('product.product', product_id, product_xmlid)
    product_id = get_res_id_from_xmlid(product_xmlid)
else:
    line_model = 'sale.order.line'
    line_vals = {
        'name': maps['projektnamn'],
        'order_id': order_id,
        'product_id': product_id,
        'price_unit': price_unit
    }
    line_xmlid = get_xmlid('migreringsprodukt', xmlid.split('_')[-1])
    if mode == 'debug':
        print(f"{line_vals=}")
        print(f"{line_xmlid=}")
    else:
        if not create_record_and_xmlid(line_model, line_vals, line_xmlid):
            write_record(line_model, line_vals, line_xmlid)
        
if maps['projekt']:
    project_vals = {
        'name': maps['projektnamn'],
        'sale_order_id': order_id,
    }
    project_xmlid = get_xmlid('projekt', maps['projekt'])
    if mode == 'debug':
        print(f"{project_vals=}")
        print(f"{project_xmlid=}")
    else:
        if not create_record_and_xmlid('project.project', project_vals, project_xmlid):
            write_record('project.project', project_vals, project_xmlid)
""",
    },
    # endregion
}
