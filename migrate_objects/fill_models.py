#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

# ~ # res.users fields to copy from source to target BROKEN
res_users_exclude = ['invoice_ids', 'message_follower_ids', 'groups_id', 'access_group_ids']
res_users_exclude_patterns = [r'\w+_\w+_\d.*']
res_users_custom = {
    'property_account_payable': 'property_account_payable_id',
    'property_account_receivable': 'property_account_receivable_id'
}
res_users_hard_code = {
    'notification_type': 'email'
}
migrate_model('res.users', include=False, create=False, custom=res_users_custom, hard_code=res_users_hard_code, migrate_fields = res_users_exclude, exclude_patterns = res_users_exclude_patterns)


if debug:
    input("press enter to continue")

# ~ # res.partner fields to copy from source to target WORKS
res_partner_exclude = ['invoice_ids', 'message_follower_ids', 'access_group_ids', 'user_ids']
res_partner_calc = {'type': """
type_val = record['type']
if type_val == 'default':
    type_val = 'contact'
vals[key] = type_val
"""}
migrate_model('res.partner', migrate_fields = res_partner_exclude, include=False, create=False, calc = res_partner_calc)


if debug:
    input("press enter to continue")

# hr.employee fields to copy from source to target WORKS
hr_employee_exclude = ['message_follower_ids']
hr_employee_custom = {
    'image_medium' : 'image_1920',
}
migrate_model('hr.employee', migrate_fields = hr_employee_exclude, include=False, create=False, custom=hr_employee_custom)


if debug:
    input("press enter to continue")

# hr.department fields to copy from source to target WORKS
migrate_model('hr.department', include=False, create=False)


if debug:
    input("press enter to continue")

# account.account.type fields to copy from source to target WORKS
account_type_hard_code = {'type': 'receivable', 'internal_group': 'equity'}
migrate_model('account.account.type', include=False, create=False, hard_code = account_type_hard_code)


if debug:
    input("press enter to continue")

# ~ # account.account fields to copy from source to target WORKS
account_custom = {'user_type': 'user_type_id'}
account_hard_code = {'reconcile': 1}
migrate_model('account.account', hard_code = account_hard_code, include=False, create=False, custom = account_custom)


if debug:
    input("press enter to continue")

# res.currency fields to copy from source to target
#migrate_model('res.currency', include=False, create=False)


if debug:
    input("press enter to continue")

# product.category fields to copy from source to target WORKS
product_category_hardcode = {
    'property_cost_method': 'standard',
    'property_valuation': 'manual_periodic'
}
#migrate_model('product.category', include=False, hard_code = product_category_hardcode, create = False)


if debug:
    input("press enter to continue")

# product.attribute fields to copy from source to target
product_attribute_custom = {'type': 'display_type'} # create variant should be hardcoded to no_variant
product_attribute_hard_code = {'create_variant': 'always'}
migrate_model('product.attribute', include=False, create=False, custom = product_attribute_custom, hard_code = product_attribute_hard_code)

if debug:
    input("press enter to continue")


# product.attribute.value fields to copy from source to target
#migrate_model('product.attribute.value', include=False, create=False)


# product.public.category fields to copy from source to target WORKS
product_public_category_custom = {
    'image_medium' : 'image_1920'
}
#migrate_model('product.public.category', custom = product_public_category_custom, include=False, create = False)

if debug:
    input("press enter to continue")

# product.template fields to copy from source to target WORKS(needs uom to be set up correctly)
product_template_exclude = ['message_follower_ids', 'company_id', 'product_variant_ids', 'product_variant_count', 'variant_access_group_ids']
product_template_custom = {
    'image_medium' : 'image_1920',
}
product_template_hardcode = {'company_id': 1}
#migrate_model('product.template', include=False, custom=product_template_custom, migrate_fields = product_template_exclude, hard_code = product_template_hardcode, create = False)

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
product_product_exclude = ['uom_po_id','message_follower_ids', 'company_id', 'attribute_value_names', 'product_variant_ids', 'virtual_available_days', 'purchase_line_warn', 'purchase_line_warn_message', 'uom_id', 'sale_line_warn', 'categ_id', 'access_group_ids']
product_product_custom = {
    'image' : 'image_1920'
}
product_product_hardcode = {}
migrate_model('product.product', include=False, custom=product_product_custom, migrate_fields = product_product_exclude, hard_code = product_product_hardcode, create = False)
if debug:
    input("press enter to continue")
migrate_model('product.product', include=True, migrate_fields = ['virtual_available_days'], create = False)

# product.pricelist fields to copy from source to target WORKS
migrate_model('product.pricelist', include=False, create=False)

if debug:
    input("press enter to continue")

# product.pricelist.item fields to copy from source to target WORKS
pricelist_item_hardcode = {'company_id': 1}
pricelist_item_calc = {'base': """
translation = {-1: 'pricelist', 1: 'list_price', 2: 'standard_price', -2: 'standard_price'}
vals[key] = translation[record['base']]
"""}
migrate_model('product.pricelist.item', include=False, create=False, calc = pricelist_item_calc, hard_code = pricelist_item_hardcode)

if debug:
    input("press enter to continue")

# stock.location fields to copy from source to target
stock_location_exclude = ['company_id']
stock_location_hardcode = {'company_id': 1}
migrate_model('stock.location', hard_code = stock_location_hardcode, migrate_fields = stock_location_exclude, include=False, create=False)

if debug:
    input("press enter to continue")

# stock.warehouse fields to copy from source to target
stock_warehouse_exclude = ['company_id']
stock_warehouse_hardcode = {'company_id': 1}
migrate_model('stock.warehouse', hard_code = stock_warehouse_hardcode, migrate_fields = stock_warehouse_exclude, include=False, create=False)

if debug:
    input("press enter to continue")

# sale.order fields to copy from source to target
sale_order_exclude = ['message_follower_ids', 'message_is_follower']
migrate_model('sale.order', include=False, exclude = sale_order_exclude, create=False)

if debug:
    input("press enter to continue")

# sale.order.line fields to copy from source to target
sale_order_line_custom = {
    'delay': 'customer_lead'
}
migrate_model('sale.order.line', include=False, create=False, custom = sale_order_line_custom)





