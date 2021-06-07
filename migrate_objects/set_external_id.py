#!/usr/bin/env python3

from configuration import *

# ~ # pricelist item fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ uom_fields = {
    # ~ 'factor': 'factor',
    # ~ 'factor_inv': 'factor_inv',
    # ~ 'name': 'name',
    # ~ 'rounding': 'rounding',
# ~ }

# ~ # attribute fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ attribute_fields = {
    # ~ 'name': 'name',
    # ~ 'type': 'display_type',
# ~ }

# ~ # attribute value fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ attribute_value_fields = {
    # ~ 'name': 'name',
# ~ }

# ~ # attribute line fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ attribute_line_fields = {
    # ~ 'id' : 'id',
    # ~ 'display_name' : 'display_name',
    # ~ 'active' : 'active',
# ~ }

# ~ # pricelist fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ pricelist_fields = {
    # ~ 'name' : 'name',
    # ~ 'code': 'code',
    # ~ 'display_name': 'display_name',
# ~ }

# ~ # pricelist item fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ pricelist_item_fields = {
    # ~ 'price_discount': 'price_discount',
    # ~ 'price_round': 'price_round',
    # ~ 'price_discount': 'price_discount',
    # ~ 'price_min_margin': 'price_min_margin',
    # ~ 'price_max_margin': 'price_max_margin',
# ~ }

# ~ # variant fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ variant_fields = {
    # ~ 'name' : 'name',
    # ~ 'sale_ok' : 'sale_ok',
    # ~ 'description' : 'description',
    # ~ 'purchase_ok': 'purchase_ok',
    # ~ 'list_price': 'list_price',
    # ~ 'description_sale': 'description_sale',
    # ~ 'default_code': 'default_code',
    # ~ # 'image' : 'image_1920',
    # ~ 'active' : 'active',
    # ~ 'website_published': 'website_published',
    # ~ 'product_tmpl_id': 'product_tmpl_id',
    # ~ # added later:
    # ~ 'default_code' : 'default_code',
    # ~ 'lst_price' : 'lst_price',
    # ~ 'volume' : 'volume',
    # ~ 'attribute_value_ids': 'attribute_value_ids',
    # ~ # 'available_in_pos' : 'available_in_pos',
    # ~ # 'weight' : 'weight',
    # ~ # 'ingredients': 'ingredients',
    # ~ # 'ingredients_last_changed': 'ingredients_last_changed',
    # ~ # 'ingredients_changed_by_uid':'ingredients_changed_by_uid',
    # ~ # 'use_desc': 'use_desc',
    # ~ # 'use_desc_last_changed': 'use_desc_last_changed',
    # ~ # 'use_desc_changed_by_uid': 'use_desc_changed_by_uid',
    # ~ # 'event_ok': 'event_ok',
    # ~ 'standard_price': 'standard_price',
# ~ }

# ~ # template fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ template_fields = {
    # ~ 'name' : 'name',
    # ~ 'sale_ok' : 'sale_ok',
    # ~ 'description' : 'description',
    # ~ 'purchase_ok': 'purchase_ok',
    # ~ 'list_price': 'list_price',
    # ~ 'standard_price' : 'standard_price',
    # ~ 'description_sale': 'description_sale',
    # ~ 'default_code': 'default_code',
    # ~ 'image_medium' : 'image_1920',
    # ~ 'website_published': 'website_published',
    # ~ 'active' : 'active',
# ~ }

# ~ # Groups fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ groups_fields = {
    # ~ 'name' : 'name',
# ~ }

# ~ # category fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ category_fields = {
    # ~ 'name' : 'name',
    # ~ 'display_name' : 'display_name',
# ~ }

# ~ # tax fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ taxes_fields = {
    # ~ 'name' : 'name',
    # ~ 'sale_ok' : 'sale_ok',
    # ~ 'amount': 'amount',
    # ~ 'sequence': 'sequence',
    # ~ 'description': 'description',
# ~ }

# ~ # tax fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ tax_group_fields = {
    # ~ 'name' : 'name',
# ~ }

# ~ # company fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ company_fields = {
    # ~ 'create_date' : 'account_opening_date',
    # ~ 'manufacturing_lead': 'manufacturing_lead',
    # ~ 'name': 'name',
    # ~ 'po_lead': 'po_lead',
    # ~ 'security_lead': 'security_lead',
# ~ }

# ~ # res currency fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ res_currency_fields = {
    # ~ 'name' : 'name',
    # ~ 'symbol' : 'symbol',
# ~ }

# ~ # account fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ account_fields = {
    # ~ 'code' : 'code',
    # ~ 'name' : 'name',
# ~ }

# ~ # account type fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ account_type_fields = {
    # ~ 'name' : 'name',
# ~ }


# ~ # sale fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ sale_order_fields = {
    # ~ 'name' : 'name',
    # ~ 'date_order': 'date_order',
# ~ }
# ~ # sale order line fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ sale_order_line_fields = {
    # ~ 'name' : 'name',
    # ~ 'price_unit': 'price_unit',
# ~ }

# ~ # stock warehouse fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ stock_warehouse_fields = {
    # ~ 'name' : 'name',
    # ~ 'code': 'code',
# ~ }


# ~ # sale order line fields to copy from source to target
# ~ # { 'source_field_name' : 'target_field_name' }
# ~ location_fields = {
    # ~ 'name' : 'name',
# ~ }
# ---------------------------------------------------------------------------
# this code replaces res.company at target with source
# ---------------------------------------------------------------------------

# company fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
# ~ model = 'res.company'
# ~ res_company = source.env[model].browse(1)
# ~ fields = {
    # ~ 'create_date' : 'account_opening_date',
    # ~ 'manufacturing_lead': 'manufacturing_lead',
    # ~ 'name': 'name',
    # ~ 'po_lead': 'po_lead',
    # ~ 'security_lead': 'security_lead',
# ~ }
# ~ vals = source.env[model].read(1, fields)
# ~ vals.update({'country_id': get_id_from_xml_id(res_company.country_id)})
# ~ vals.update({'currency_id': get_id_from_xml_id(res_company.currency_id)})
# ~ vals.update({'paperformat_id': target.env.ref('base.paperformat_euro').id})
# ~ target.env[model].browse(1).write(vals)

# res.partner fields to copy from source to target WORKS
res_partner_fields = ['name', 'email', 'mobile', 'phone', 'street', 'city', 'zip']
# ~ migrate_model('res.partner', migrate_fields= res_partner_fields, include=True)

# hr.employee fields to copy from source to target WORKS
hr_employee_fields = ['name', 'work_email', 'mobile_phone', 'work_location', 'company_id']
hr_employee_custom = {
    'image_medium' : 'image_1920',
}
# ~ migrate_model('hr.employee', migrate_fields = hr_employee_fields, include=True, custom=hr_employee_custom)

# account.account.type fields to copy from source to target WORKING
account_type_field = ['name']
account_type_hard_code = {'type': 'receivable', 'internal_group': 'equity'}
# ~ migrate_model('account.account.type', migrate_fields = account_type_field, include=True, hard_code = account_type_hard_code)

# account.account fields to copy from source to target WORKING
account_fields = ['code', 'name', 'company_id']
account_custom = {'user_type': 'user_type_id'}
account_hard_code = {'reconcile': 1}
# ~ migrate_model('account.account', migrate_fields = account_fields, hard_code = account_hard_code, include=True, custom = account_custom)

# product.pricelist fields to copy from source to target WORKING
product_pricelist_fields = ['name', 'code', 'display_name']
# ~ migrate_model('product.pricelist',migrate_fields = product_pricelist_fields, include=True, )

# product.pricelist.item fields to copy from source to target WORKING
product_pricelist_item_fields = ['price_discount', 'price_round', 'price_discount', 'price_min_margin', 'price_max_margin']
# ~ migrate_model('product.pricelist.item', migrate_fields = product_pricelist_item_fields , include=True, )

# res.currency fields to copy from source to target WORKING i think?
res_currency_fields = ['name', 'symbol']
# ~ migrate_model('res.currency', migrate_fields = res_currency_fields, include=True, )

# stock.location fields to copy from source to target WORKING
stock_location_fields = ['name', 'usage']
# ~ migrate_model('stock.location', migrate_fields = stock_location_fields, include=True, )

# stock.warehouse fields to copy from source to target WORKING
stock_warehouse_fields = ['name', 'code', 'view_location_id', 'delivery_steps', 'reception_steps', 'partner_id', 'lot_stock_id', 'view_location_id']
# ~ migrate_model('stock.warehouse', migrate_fields = stock_warehouse_fields, include=True, )

# sale.order fields to copy from source to target WORKING
sale_order_fields = ['name', 'date_order', 'company_id', 'partner_id', 'partner_shipping_id', 'partner_invoice_id', 'picking_policy', 'pricelist_id', 'warehouse_id']
# ~ migrate_model('sale.order', migrate_fields = sale_order_fields, include=True, )

# sale.order.line fields to copy from source to target NEEDS sale.order fully migrated
sale_order_line_fields = ['name', 'price_unit', 'product_uom_qty', 'order_id', 'company_id']
account_custom = {
    'delay': 'customer_lead'
}
# ~ SELECT con.*
       # ~ FROM pg_catalog.pg_constraint con
            # ~ INNER JOIN pg_catalog.pg_class rel
                       # ~ ON rel.oid = con.conrelid
            # ~ INNER JOIN pg_catalog.pg_namespace nsp
                       # ~ ON nsp.oid = connamespace
       # ~ WHERE nsp.nspname = '<schema name>'
             # ~ AND rel.relname = '<table name>';
migrate_model('sale.order.line', migrate_fields = sale_order_line_fields, include=True, custom = account_custom, hard_code = {'product_id': 45})

# account.tax.group fields to copy from source to target BROKEN
account_tax_group_fields = ['name']
# ~ migrate_model('account.tax.group', migrate_fields = account_tax_group_fields, include=True, )

# account.tax fields to copy from source to target BROKEN
account_tax_fields = ['name', 'amount', 'sequence', 'description']
# ~ migrate_model('account.tax', migrate_fields = account_tax_fields, include=True, )

# uom.category fields to copy from source to target 
uom_category_fields = []
# ~ migrate_model({'product.uom.categ':'uom.category'}, migrate_fields = uom_category_fields, include=False) #needs handling for different model names on different databases

# uom.uom fields to copy from source to target NEEDS to migrate the records with uom_type == "reference" first
uom_uom_fields = ['id']
# ~ migrate_model({'product.uom':'uom.uom'}, migrate_fields = uom_uom_fields, include=False, ) #needs handling for different model names on different databases

# res.groups fields to copy from source to target WORKING
res_groups_fields = ['name']
# ~ migrate_model('res.groups', migrate_fields = res_groups_fields, include=True, )

# product.public.category fields to copy from source to target WORKING
product_public_category_fields = ['name', 'display_name']
# ~ migrate_model('product.public.category', migrate_fields = product_public_category_fields, include=True, )

# product.attribute fields to copy from source to target WORKING
product_attribute_fields = ['name']
product_attribute_custom = {'type': 'display_type'} # create variant should be hardcoded to no_variant
product_attribute_hard_code = {'create_variant': 'always'}
# ~ migrate_model('product.attribute', migrate_fields = product_attribute_fields, include=True, custom = product_attribute_custom, hard_code = product_attribute_hard_code)

# product.attribute.value fields to copy from source to target WORKING
product_attribute_value_fields = ['name', 'attribute_id']
# ~ migrate_model('product.attribute.value', migrate_fields = product_attribute_value_fields, include=True, )

# product.category fields to copy from source to target
product_category_fields = ['name']
product_category_custom = {
}
product_category_hard_code = {
    'property_cost_method': 'standard',
    'property_valuation': 'manual_periodic'
}
# ~ migrate_model('product.category', migrate_fields = product_category_fields, include=True, hard_code = product_category_hard_code)

# product.template fields to copy from source to target NEEDS uom.uom to be migrated, which is product.uom on odoo8
product_template_fields = ['name', 'sale_ok', 'purchase_ok', 'list_price', 'standard_price', 'description_sale', 'default_code', 'website_published', 'active', 'type', 'categ_id', 'sale_line_warn', 'tracking']
product_template_custom = {
    'image_medium' : 'image_1920',
}
product_template_hard_code = {'product_variant_ids': []}
# ~ migrate_model('product.template', migrate_fields = product_template_fields, include=True, custom = product_template_custom) #the old one had some weird checks for default code? incase it doesnt work

# product.product fields to copy from source to target
product_product_fields = ['name', 'sale_ok', 'description', 'purchase_ok', 'list_price', 'description_sale', 'default_code', 'active',
'website_published', 'product_tmpl_id', 'lst_price', 'volume', 'attribute_value_ids', 'standard_price', 'available_in_pos', 'weight',
'ingredients', 'ingredients_last_changed', 'ingredients_changed_by_uid', 'use_desc', 'use_desc_last_changed', 'use_desc_changed_by_uid', 'event_ok']
product_product_custom = {
    'image' : 'image_1920'
}
# ~ migrate_model('product.product', migrate_fields = product_product_fields, include=True, custom = product_product_custom)
#
# if default_variant_ids:
#     target.env['product.product'].browse(default_variant_ids).unlink()
