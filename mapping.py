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
            'kurs.idkurs': 'kurs.idkurs'
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

maps['event_xmlid'] = get_xmlid('idkurs', vals.pop('kurs.idkurs'))
""",
        'post_sync': """
event_id = get_res_id_from_xmlid(maps.get('event_xmlid'))
partner_id = get_res_id_from_xmlid(xmlid)
if event_id and partner_id:
    er_model = 'event.registration'
    er_vals = {
        'event_id': event_id,
        'partner_id': partner_id,
        }
    er_xmlid = get_xmlid('kursdeltagare_kurs', xmlid.split('_')[-1])
    if mode == 'debug':
        print(f"{er_vals=}")
        print(f"{er_xmlid=}")
    else:
        if not create_record_and_xmlid(er_model, er_vals, er_xmlid):
            write_record(er_model, er_vals, er_xmlid)
""",
    },
    # endregion
    # region fafast.xlsx
    'idfafast': {
        'model': 'property.property',
        'fields': {
            'name': 'namnfast',
            'property_key': 'fastnr',
            'latitude': 'xkoordinat',
            'longitude': 'ykoordinat',
        },
        'pre_sync': """
latitude = str(vals.pop('latitude'))
longitude = str(vals.pop('longitude'))
name = str(vals['name'])

if name and ',' in name:
    vals['city'] = name.split(',')[0]
    
if latitude and len(latitude) == 7:
    latitude = f"{latitude[:2]}.{latitude[2:]}"
    vals['latitude'] = latitude

if longitude and len(longitude) == 7:
    longitude = f"{longitude[:2]}.{longitude[2:]}"
    vals['longitude'] = longitude
    
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
    uid = vals['user_id']
    if uid:
        uid = target.env['res.users'].search([('login', '=', uid)])
        if uid:
            vals['user_id'] = uid[0]
    if not uid:
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
            'parent_template_id': 'produkt.idprodukt',
            'uom_id': 'enhet',
        },
        'pre_sync': """
vals['list_price'] = float(vals['list_price'].split(',')[0].replace('.',''))
vals['property_account_expense_id'] = get_res_id_from_xmlid('l10n_se.1_chart4001')
vals['property_account_income_id'] = get_res_id_from_xmlid('l10n_se.1_chart3001')
vals['service_policy'] = 'delivered_timesheet'
vals['service_tracking'] = 'task_in_project'

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
maps['parent_template_xmlid'] = get_xmlid('idprod_reg', vals.pop('parent_template_id'))
""",
        'post_sync': """
template_id = get_res_id_from_xmlid(xmlid)
if template_id:
    template = target.env['product.template'].read(template_id)[0]
    product_id = template['product_variant_id'][0]
    if product_id:
        parent_template_id = get_res_id_from_xmlid(maps.get('parent_template_xmlid'))
        if parent_template_id:
            parent_template = target.env['product.template'].read(parent_template_id)[0]
            parent_product_id = parent_template['product_variant_id'][0]
            if parent_product_id:
                pl_xmlid = get_xmlid('artikel', xmlid.split('_')[-1])
                pl_model = 'product.pack.line'
                pl_vals = {
                    'parent_product_id': parent_product_id, 
                    'product_id': product_id,
                    }
            if mode == 'debug':
                print(f"{pl_vals=}")
            else:
                if not create_record_and_xmlid(pl_model, pl_vals, pl_xmlid):
                    write_record(pl_model, pl_vals, pl_xmlid)
""",
    },
    # endregion
    # region prod_reg.xlsx
    'idprod_reg': {
        'model': 'product.template',
        'fields': {
            'name': 'namn',
            'description': 'intern_beskrivning',
            'description_sale': 'beskrivning',
            'verksamhetsgren': 'verksamhetsgren',
        },
        'pre_sync': """
categ_xmlid = get_xmlid('product_category', vals.pop('verksamhetsgren'))
categ_id = get_res_id_from_xmlid(categ_xmlid)
if categ_id:
    vals['categ_id'] = categ_id
vals['pack_ok'] = True
vals['pack_type'] = 'detailed'
vals['pack_component_price'] = 'detailed'
vals['pack_modifiable'] = True
""",
    },
    # endregion
    # region uppdrag.xlsx
    'iduppdrag': {
        'model': 'sale.order',
        'fields': {
            'summa': 'summa_fakturerat',
            'note': 'annan_info',
            'partner_id': 'kund.idkund',
            'projekt': 'projekt',
            'projektnamn': 'uppdragsbenamning',
            'user_id': 'ansvarig_medarbetare.anvandare',
        },
        'pre_sync': """
partner_xmlid = get_xmlid('idkund', vals['partner_id'])
vals['partner_id'] = get_res_id_from_xmlid(partner_xmlid)
if not vals['partner_id']:
    vals['skip'] = True

uid = vals['user_id']
if uid:
    uid = target.env['res.users'].search([('login', '=', uid)])
    if uid:
        vals['user_id'] = uid[0]
if not uid:
    vals.pop('user_id')

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
    project_id = get_res_id_from_xmlid(project_xmlid)
    if project_id:
        target.env['sale.order'].write(order_id, {'project_id': project_id})
""",
    },
    # endregion
    # region verksamhetsgrenar.xlsx
    'product_category': {
        'model': 'product.category',
        'fields': {
            'name': 'Beskrivning',
            },
        'pre_sync': """
vals['parent_id'] = 11
""",
    },
    # endregion
}
