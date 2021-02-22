#!/usr/bin/env python3

from configuration import *

# uom fields to copy from source to target
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
    'image_medium' : 'image_1920',
    'active' : 'active',
    'website_published': 'website_published',

    # added later:
    'default_code' : 'default_code',
    'lst_price' : 'lst_price',
    'volume' : 'volume',
    'available_in_pos' : 'available_in_pos',
    'weight' : 'weight',
    'ingredients': 'ingredients',
    'ingredients_last_changed': 'ingredients_last_changed',
    'ingredients_changed_by_uid':'ingredients_changed_by_uid',
    'use_desc': 'use_desc',
    'use_desc_last_changed': 'use_desc_last_changed',
    'use_desc_changed_by_uid': 'use_desc_changed_by_uid',
    'event_ok': 'event_ok',
    'reseller_desc':'reseller_desc',
    'reseller_desc_last_changed': 'reseller_desc_last_changed',
    'reseller_desc_changed_by_uid': 'reseller_desc_changed_by_uid',
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

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
taxes_fields = {
    'name' : 'name', 
    'sale_ok' : 'sale_ok',
    'amount': 'amount',
    'sequence': 'sequence',
    'description': 'description',
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
tax_group_fields = {
    'name' : 'name', 
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
company_fields = {
    'create_date' : 'account_opening_date', 
    'fiscalyear_last_day': 'fiscalyear_last_day',
    'fiscalyear_last_month': 'fiscalyear_last_month',
    'manufacturing_lead': 'manufacturing_lead',
    'name': 'name',
    'po_lead': 'po_lead',
    'security_lead': 'security_lead',
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
res_currency_fields = {
    'name' : 'name', 
    'symbol' : 'symbol',
}


# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
res_partner_fields = {
    'name' : 'name', 
    'symbol' : 'symbol',
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
sale_order_fields = {
    'name' : 'name', 
    'date_order': 'date_order',
    'currency_id': 


}



# for source_order_id in source.env['sale.order'].search([]):
#     source_order = source.env['sale.order'].read(source_order_id, list(res_currency_fields.keys()))
#     fields = {res_currency_fields[key] : source_currency[key] for key in res_currency_fields.keys() }
#     create_record_and_xml_id('sale.order', fields, source_currency_id)
# print()


# for source_currency_id in source.env['res.currency'].search([]):
#     source_currency = source.env['res.currency'].read(source_currency_id, list(res_currency_fields.keys()))
#     fields = {res_currency_fields[key] : source_currency[key] for key in res_currency_fields.keys() }
#     create_record_and_xml_id('res.currency', fields, source_currency_id)
# print()

# for source_partner_id in source.env['res.partner'].search([]):
#     source_partner = source.env['res.partner'].read(source_partner_id, list(res_partner_fields.keys()))
#     fields = {res_partner_fields[key] : source_partner[key] for key in res_partner_fields.keys() }
#     create_record_and_xml_id('res.partner', fields, source_partner_id)
# print()

# # product.attribute.value
# for source_company_id in source.env['res.company'].search([]):
#     source_company = source.env['res.company'].read(source_company_id, list(company_fields.keys()) + ['currency_id', 'partner_id'])
#     source_attribute = source.env['res.company'].read(source_company['currency_id'][0], ['id'])
#     fields = {company_fields[key] : source_company[key] for key in company_fields.keys() }
#     fields.update({'currency_id': get_target_record_from_id('res.currency', source_company['id']).id})
#     fields.update({'partner_id': get_target_record_from_id('res.partner', source_company['id']).id})
#     try:
#         create_record_and_xml_id('res.company', fields, source_cvariant_fieldsompany_id)
#     except:
#         print("ERROR: could not write res.company. Entry probably already exist.")
# print()

# for source_account_tax_group_id in source.env['account.tax.group'].search([]):
#     source_tax_group = source.env['account.tax.group'].read(source_account_tax_group_id, list(tax_group_fields.keys()))
#     fields = { template_fields[key] : source_tax_group[key] for key in tax_group_fields.keys() }
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

for source_uom_id in source.env['uom.uom'].search([]):
    source_uom = source.env['uom.uom'].read(source_uom_id, list(uom_fields.keys()) + ['category_id'])
    fields = {uom_fields[key] : source_uom[key] for key in uom_fields.keys()}
    fields.update({'uom_type': 'bigger'})
    fields.update({'category_id': get_target_record_from_id('product.public.category', source_uom['category_id']).id})
    create_record_and_xml_id('uom.uom', fields, source_uom_id)
print()
exit()
    
for source_variant_id in source.env['product.product'].search([]):
    source_variant = source.env['product.product'].read(source_variant_id, list(variant_fields.keys()))
    fields = {variant_fields[key] : source_variant[key] for key in variant_fields.keys() }
    create_record_and_xml_id('product.product', fields, source_variant_id)
print()

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    fields = {template_fields[key] : source_template[key] for key in template_fields.keys() }
    create_record_and_xml_id('product.template', fields, source_template_id)
print()

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

for source_pricelist_id in source.env['product.pricelist'].search([]):
    source_pricelist = source.env['product.pricelist'].read(source_pricelist_id, list(pricelist_fields.keys()))
    fields = {pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys() }
    create_record_and_xml_id('product.pricelist', fields, source_pricelist_id)
print()

for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, list(pricelist_item_fields.keys()))
    fields = {pricelist_item_fields[key] : source_pricelist_item[key] for key in pricelist_item_fields.keys()}
    create_record_and_xml_id('product.pricelist.item', fields, source_pricelist_item_id)
print()

for source_attribute_id in source.env['product.attribute'].search([]):
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))    
    fields = {target_f : source_attribute[source_f] for source_f, target_f in attribute_fields.items()}
    fields.update({'create_variant': 'no_variant'})
    create_record_and_xml_id('product.attribute', fields, source_attribute_id)
print()

# product.attribute.value
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

# product.template.attribute.line
for source_attribute_line_id in source.env['product.attribute.line'].search([]):
    source_attribute_line = source.env['product.attribute.line'].read(source_attribute_line_id, ['id', 'attribute_id', 'value_ids', 'product_tmpl_id'])
    
    target_attribute_line_tmpl = get_target_record_from_id('product.template', source_attribute_line['product_tmpl_id'][0])
    
    if not target_attribute_line_tmpl:
        print("Found attribute line without a product.template. Skipping creation.")
        continue
        
    target_attribute_line_attribute_id = get_target_record_from_id('product.attribute', source_attribute_line['attribute_id'][0]).id
    
    try:
        target_attribute_line_value_ids = [ get_target_record_from_id('product.attribute.value', val).id for val in source_attribute_line['value_ids'] ]
    except:
        continue
    
    fields = { 'product_tmpl_id': target_attribute_line_tmpl.id, 'attribute_id' : target_attribute_line_attribute_id, 'value_ids': target_attribute_line_value_ids}
    create_record_and_xml_id('product.template.attribute.line', fields, source_attribute_line['id'])

