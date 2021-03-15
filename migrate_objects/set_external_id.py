#!/usr/bin/env python3

from configuration import *


# pricelist item fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
uom_fields = {
    'factor': 'factor',
    'factor_inv': 'factor_inv',
    'name': 'name',
    'rounding': 'rounding',
}

# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_fields = {
    'name': 'name',
    'type': 'display_type',
}

# attribute value fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_value_fields = {
    'name': 'name',
}

# attribute line fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_line_fields = {
    'id' : 'id',
    'display_name' : 'display_name',
    'active' : 'active',
}

# pricelist fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
pricelist_fields = {
    'name' : 'name',
    'code': 'code',
    'display_name': 'display_name',
}

# pricelist item fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
pricelist_item_fields = {
    'price_discount': 'price_discount',
    'price_round': 'price_round',
    'price_discount': 'price_discount',
    'price_min_margin': 'price_min_margin',
    'price_max_margin': 'price_max_margin',
}

# variant fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
variant_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    # 'image' : 'image_1920',
    'active' : 'active',
    'website_published': 'website_published',
    'product_tmpl_id': 'product_tmpl_id',
    # added later:
    'default_code' : 'default_code',
    'lst_price' : 'lst_price',
    'volume' : 'volume',
    'attribute_value_ids': 'attribute_value_ids',
    # 'available_in_pos' : 'available_in_pos',
    # 'weight' : 'weight',
    # 'ingredients': 'ingredients',
    # 'ingredients_last_changed': 'ingredients_last_changed',
    # 'ingredients_changed_by_uid':'ingredients_changed_by_uid',
    # 'use_desc': 'use_desc',
    # 'use_desc_last_changed': 'use_desc_last_changed',
    # 'use_desc_changed_by_uid': 'use_desc_changed_by_uid',
    # 'event_ok': 'event_ok',
    'standard_price': 'standard_price',
}

# template fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
template_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'standard_price' : 'standard_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'image_medium' : 'image_1920',
    'website_published': 'website_published',
    'active' : 'active',
}

# Groups fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
groups_fields = {
    'name' : 'name',
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
category_fields = {
    'name' : 'name', 
    'display_name' : 'display_name',
}

# tax fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
taxes_fields = {
    'name' : 'name', 
    'sale_ok' : 'sale_ok',
    'amount': 'amount',
    'sequence': 'sequence',
    'description': 'description',
}

# tax fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
tax_group_fields = {
    'name' : 'name', 
}

# company fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
company_fields = {
    'create_date' : 'account_opening_date', 
    'manufacturing_lead': 'manufacturing_lead',
    'name': 'name',
    'po_lead': 'po_lead',
    'security_lead': 'security_lead',
}

# res currency fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
res_currency_fields = {
    'name' : 'name', 
    'symbol' : 'symbol',
}

# account fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
account_fields = {
    'code' : 'code', 
    'name' : 'name',
}

# account type fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
account_type_fields = {
    'name' : 'name',
}

# res partner fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
res_partner_fields = {
    'name' : 'name', 
    'email': 'email',
    'mobile': 'mobile',
    'phone':'phone',
    'street': 'street',
    'city': 'city',
    'zip': 'zip',
    'image': 'image_1920',
    # 'parent_id': 'parent_id',
}
# sale fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
sale_order_fields = {
    'name' : 'name',
    'date_order': 'date_order',
}
# sale order line fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
sale_order_line_fields = {
    'name' : 'name', 
    'price_unit': 'price_unit',
}

# stock warehouse fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
stock_warehouse_fields = {
    'name' : 'name', 
    'code': 'code',
}


# sale order line fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
location_fields = {
    'name' : 'name', 
}



# for source_account_type_id in source.env['account.account.type'].search([]):
#     source_account_type = source.env['account.account.type'].read(source_account_type_id, list(account_type_fields.keys()) + ['type','internal_group'])

#     fields = {account_type_fields[key] : source_account_type[key] for key in account_type_fields.keys() }
#     fields.update({'internal_group': 'equity'})
#     fields.update({'type': 'receivable'})

#     create_record_and_xml_id('account.account.type', fields, source_account_type_id)
# print()


# for source_account_id in source.env['account.account'].search([]):
#     source_account = source.env['account.account'].read(source_account_id, list(account_fields.keys()) + ['company_id','user_type'])

#     fields = {account_fields[key] : source_account[key] for key in account_fields.keys() }
#     fields.update({'user_type_id': get_target_record_from_id('account.account.type', source_account['user_type'])})
#     fields.update({'company_id': get_target_record_from_id('res.company', source_account['company_id'])})
#     try:
#         create_record_and_xml_id('account.account', fields, source_account_id)
#     except:
#         print("ERROR: could not write account.account. Entry probably already exist.")
# print()


# for source_partner_id in source.env['res.partner'].search([]):
#     source_partner = source.env['res.partner'].read(source_partner_id, list(res_partner_fields.keys()))

#     fields = {res_partner_fields[key] : source_partner[key] for key in res_partner_fields.keys() }

#     create_record_and_xml_id('res.partner', fields, source_partner_id)



for source_pricelist_id in source.env['product.pricelist'].search([]):
    source_pricelist = source.env['product.pricelist'].read(source_pricelist_id, list(pricelist_fields.keys()))
    fields = {pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys() }
    create_record_and_xml_id('product.pricelist', fields, source_pricelist_id)
print()


# for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
#     source_pricelist_value = source.env['product.pricelist.item'].read(source_pricelist_item_id, list(pricelist_item_fields.keys()) + ['base_pricelist_id'])
#     source_pricelist_base = source.env['product.pricelist.item'].read(source_pricelist_value['base_pricelist_id'][0], ['id'])
#     fields = {pricelist_item_fields[key] : source_pricelist_value[key] for key in pricelist_item_fields.keys() }
#     fields.update({'base_pricelist_id': get_target_record_from_id('product.pricelist', source_pricelist_base['id'])})
#     try:
#         create_record_and_xml_id('product.pricelist.item', fields, source_pricelist_item_id)
#     except:
#         print("ERROR: could not write product.pricelist.item. Entry probably already exist.")
# print()



# for source_currency_id in source.env['res.currency'].search([]):
#     source_currency = source.env['res.currency'].read(source_currency_id, list(res_currency_fields.keys()))
#     fields = {res_currency_fields[key] : source_currency[key] for key in res_currency_fields.keys() }
#     create_record_and_xml_id('res.currency', fields, source_currency_id)
# print()



# exit()

# for source_company_id in source.env['res.company'].search([]):
#     source_company = source.env['res.company'].read(source_company_id, list(company_fields.keys()) + ['currency_id', 'partner_id'])
#     fields = {company_fields[key] : source_company[key] for key in company_fields.keys() }
#     fields.update({'partner_id': get_target_record_from_id('res.partner', source_company['partner_id'])})
#     fields.update({'currency_id': get_target_record_from_id('res.currency', source_company['currency_id'])})
#     create_record_and_xml_id('res.company', fields, source_company_id)
# print()

for source_location_id in source.env['stock.location'].search([]):
    source_location = source.env['stock.location'].read(source_location_id, list(location_fields.keys()) + ['usage'])
    fields = {location_fields[key] : source_location[key] for key in location_fields.keys() }
    fields.update({'usage': source_location['usage']})
    try:
        create_record_and_xml_id('stock.location', fields, source_location_id)
    except:
        print("ERROR: could not write account.account. Entry probably already exist.")
print()


for source_stock_id in source.env['stock.warehouse'].search([]):
    source_stock = source.env['stock.warehouse'].read(source_stock_id, list(stock_warehouse_fields.keys()) + ['partner_id', 'view_location_id', 'lot_stock_id', 'delivery_steps', 'reception_steps'])
    fields = {stock_warehouse_fields[key] : source_stock[key] for key in stock_warehouse_fields.keys()}

    fields.update({'partner_id': get_target_record_from_id('res.partner', source_stock['partner_id'])})
    fields.update({'lot_stock_id': get_target_record_from_id('stock.location', source_stock['lot_stock_id'])})
    fields.update({'view_location_id': get_target_record_from_id('stock.location', source_stock['view_location_id'])})
    fields.update({'delivery_steps': source_stock['delivery_steps']})
    fields.update({'reception_steps': source_stock['reception_steps']})

    create_record_and_xml_id('stock.warehouse', fields, source_stock_id)
print()

exit()





# for source_order_id in source.env['sale.order'].search([]):
#     source_order = source.env['sale.order'].read(source_order_id, list(sale_order_fields.keys()) + ['company_id', 'partner_id', 'partner_shipping_id', 'partner_invoice_id', 'picking_policy', 'pricelist_id', 'warehouse_id'])
#     fields = {sale_order_fields[key] : source_order[key] for key in sale_order_fields.keys()}
#     # print(source_order)
#     print(get_target_record_from_id('res.partner', source_order['partner_id']))

#     fields.update({'company_id': get_target_record_from_id('res.company', source_order['company_id'])})
#     fields.update({'partner_id': get_target_record_from_id('res.partner', source_order['partner_id'])})
#     fields.update({'partner_invoice_id': get_target_record_from_id('res.partner', source_order['partner_invoice_id'])})
#     fields.update({'partner_shipping_id': get_target_record_from_id('res.partner', source_order['partner_shipping_id'])})
#     fields.update({'picking_policy': source_order['picking_policy']})
#     fields.update({'pricelist_id': get_target_record_from_id('product.pricelist', source_order['pricelist_id'])})
#     fields.update({'warehouse_id': get_target_record_from_id('stock.warehouse', source_order['warehouse_id'])})
#     create_record_and_xml_id('sale.order', fields, source_order_id)
# print()

# for source_order_line_id in source.env['sale.order.line'].search([]):
#     source_order_line = source.env['sale.order.line'].read(source_order_line_id, list(sale_order_line_fields.keys()))
#     fields = {sale_order_line_fields[key] : source_order_line[key] for key in sale_order_line_fields.keys() }
#     create_record_and_xml_id('sale.order.line', fields, source_order_line_id)
# print()

# for source_account_tax_group_id in source.env['account.tax.group'].search([]):
#     source_tax_group = source.env['account.tax.group'].read(source_account_tax_group_id, list(tax_group_fields.keys()))
#     fields = { tax_group_fields[key] : source_tax_group[key] for key in tax_group_fields.keys() }
#     create_record_and_xml_id('account.tax.group', fields, source_account_tax_group_id)
# print()

# for source_account_tax_id in source.env['account.tax'].search([]):
#     source_account_tax = source.env['account.tax'].read(source_account_tax_id, list(taxes_fields.keys()) + ['tax_group_id', 'company_id', 'type_tax_use', 'type'])
#     fields = {taxes_fields[key] : source_account_tax[key] for key in taxes_fields.keys()}

#     fields.update({'tax_group_id': get_target_record_from_id('account.tax.group', source_account_tax['tax_group_id']).id})
#     fields.update({'company_id': get_target_record_from_id('res.company', source_account_tax['company_id']).id})
#     fields.update({'type_tax_use': source_account_tax['type_tax_use']})
#     fields.update({'amount_type': source_account_tax['type']})

#     create_record_and_xml_id('account.tax', fields, source_account_tax_id)
# print()

# for source_uom_id in source.env['uom.uom'].search([]):
#     source_uom = source.env['uom.uom'].read(source_uom_id, list(uom_fields.keys()) + ['category_id'])
#     fields = {uom_fields[key] : source_uom[key] for key in uom_fields.keys()}
#     fields.update({'uom_type': 'bigger'})
#     fields.update({'category_id': get_target_record_from_id('product.public.category', source_uom['category_id']).id})
#     create_record_and_xml_id('uom.uom', fields, source_uom_id)
# print()




for source_groups_id in source.env['res.groups'].search([]):
    source_groups = source.env['res.groups'].read(source_groups_id, list(groups_fields.keys()))
    fields = {groups_fields[key] : source_groups[key] for key in groups_fields.keys() }
    create_record_and_xml_id('res.groups', fields, source_groups_id)
print()

for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, list(category_fields.keys()))
    fields = {category_fields[key] : source_category[key] for key in category_fields.keys() } 
    create_record_and_xml_id('product.public.category', fields, source_category_id)
print()


for source_attribute_id in source.env['product.attribute'].search([]):
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))    
    fields = {target_f : source_attribute[source_f] for source_f, target_f in attribute_fields.items()}
    fields.update({'create_variant': 'no_variant'})
    create_record_and_xml_id('product.attribute', fields, source_attribute_id)
print()


for source_attribute_value_id in source.env['product.attribute.value'].search([]):
    source_attribute_value = source.env['product.attribute.value'].read(source_attribute_value_id, list(attribute_value_fields.keys()) + ['attribute_id'])
    source_attribute = source.env['product.attribute.value'].read(source_attribute_value['attribute_id'][0], ['id'])
    fields = {attribute_value_fields[key] : source_attribute_value[key] for key in attribute_value_fields.keys() }
    fields.update({'attribute_id': get_target_record_from_id('product.attribute', source_attribute['id']).id})
    try:
        create_record_and_xml_id('product.attribute.value', fields, source_attribute_value_id)
    except:
        print("ERROR: could not write product.attribute.value. Entry probably already exist.")
print()


template_ids = []
default_variant_ids = []
for source_template_id in source.env['product.template'].search([]):
    template_ids.append(source_template_id)
    if get_target_record_from_id('product.template', source_template_id):
        continue
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    values = {template_fields[key] : source_template[key] for key in template_fields.keys() }
    values['attribute_line_ids'] = []
    for line_id in source.env['product.attribute.line'].search([('product_tmpl_id', '=', source_template_id)]):
        line = source.env['product.attribute.line'].read(line_id)
        value_ids = [get_target_record_from_id('product.attribute.value', id).id for id in line['value_ids']]
         #raise Warning(line['attribute_id'])
        attr_values = {
            'attribute_id': get_target_record_from_id('product.attribute', line['attribute_id'][0]).id,
            'value_ids': [(6, 0, value_ids)]
        }
        values['attribute_line_ids'].append((0, 0, attr_values))
    create_record_and_xml_id('product.template', values, source_template_id)
    template = get_target_record_from_id('product.template', source_template_id)
    if template: 
        default_variant_ids.append(template.product_variant_ids.id)

print()

for source_product_id in source.env['product.product'].search([('product_tmpl_id', 'in', template_ids)]):
    source_product = source.env['product.product'].read(source_product_id, list(variant_fields.keys()))
    values = {variant_fields[key] : source_product[key] for key in variant_fields.keys() }
    template = get_target_record_from_id('product.template', values['product_tmpl_id'][0])
    if not template: 
        continue
    values['product_tmpl_id'] = template.id
    values['attribute_value_ids'] = [get_target_record_from_id('product.attribute.value', id).id for id in values['attribute_value_ids']]
    attribute_value_ids = []
    for attr_id in values['attribute_value_ids']:
        attr_val_id = target.env['product.template.attribute.value'].search([('product_tmpl_id', '=', template.id), ('product_attribute_value_id', '=', attr_id)])
        if len(attr_val_id) == 0:
            print('Failed to find attr')
            continue
        attr_val_id = attr_val_id[0]
        attribute_value_ids.append(attr_val_id)
    values['product_template_attribute_value_ids'] = [(6, 0, attribute_value_ids)]
    del values['attribute_value_ids']
    create_record_and_xml_id('product.product', values, source_product_id)
print()
if default_variant_ids:
    target.env['product.product'].browse(default_variant_ids).unlink()


