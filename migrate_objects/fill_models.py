#!/usr/bin/env python3

from configuration import *


# ~ # product.category fields to copy from source to target
# ~ product_category_fields = ['name']
# ~ product_category_custom = {
# ~ }
# ~ product_category_hard_code = {
    # ~ 'property_cost_method': 'standard',
    # ~ 'property_valuation': 'manual_periodic'
# ~ }
# ~ migrate_model('product.category', migrate_fields = product_category_fields, include=True, hard_code = product_category_hard_code)


# product.category fields to sync from source to target

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

migrate_model('product.category', include=False, create = False)


product_public_category_custom = {
    'image_medium' : 'image_1920'
}
migrate_model('product.public.category', custom = product_public_category_custom, include=False, )



# res.partner fields to copy from source to target WORKS
res_partner_exclude = ['invoice_ids', '']
migrate_model('res.partner', migrate_fields = res_partner_exclude, include=False, create=False)

if debug:
    input("press enter to continue")

# hr.employee fields to copy from source to target WORKS
hr_employee_custom = {
    'image_medium' : 'image_1920',
}
migrate_model('hr.employee', include=False, create=False, custom=hr_employee_custom)

if debug:
    input("press enter to continue")

# hr.department fields to copy from source to target WORKS
migrate_model('hr.department', include=False, create=False)

if debug:
    input("press enter to continue")

# account.account.type fields to copy from source to target WORKING
account_type_hard_code = {'type': 'receivable', 'internal_group': 'equity'}
migrate_model('account.account.type', include=False, create=False, hard_code = account_type_hard_code)

if debug:
    input("press enter to continue")

# account.account fields to copy from source to target WORKING
account_custom = {'user_type': 'user_type_id'}
account_hard_code = {'reconcile': 1}
migrate_model('account.account', hard_code = account_hard_code, include=False, create=False, custom = account_custom)

if debug:
    input("press enter to continue")

# res.users fields to copy from source to target WORKS
res_users_custom = {
    'property_account_payable': 'property_account_payable_id',
    'property_account_receivable': 'property_account_receivable_id'
}
res_users_hard_code = {
    'notification_type': 'email'
}
migrate_model('res.users', include=False, create=False, custom=res_users_custom, hard_code=res_users_hard_code)

if debug:
    input("press enter to continue")

# product.pricelist fields to copy from source to target WORKING
migrate_model('product.pricelist', include=False, create=False)

if debug:
    input("press enter to continue")

# product.pricelist.item fields to copy from source to target WORKING
migrate_model('product.pricelist.item', include=False, create=False, )

if debug:
    input("press enter to continue")

# res.currency fields to copy from source to target WORKING i think?
migrate_model('res.currency', include=False, create=False)

if debug:
    input("press enter to continue")

# stock.location fields to copy from source to target WORKING
migrate_model('stock.location', include=False, create=False)

if debug:
    input("press enter to continue")

# stock.warehouse fields to copy from source to target WORKING
migrate_model('stock.warehouse', include=False, create=False)

if debug:
    input("press enter to continue")

# sale.order fields to copy from source to target WORKING
migrate_model('sale.order', include=False, create=False)

if debug:
    input("press enter to continue")

# sale.order.line fields to copy from source to target NEEDS sale.order fully migrated
account_custom = {
    'delay': 'customer_lead'
}
migrate_model('sale.order.line', include=False, create=False, custom = account_custom)

if debug:
    input("press enter to continue")

# ~ # account.tax.group fields to copy from source to target BROKEN
# ~ account_tax_group_fields = ['name']
# ~ account_tax_group_unique = 'name'
# ~ # migrate_model('account.tax.group', migrate_fields = account_tax_group_fields, include=True, unique = account_tax_group_unique)

if debug:
    input("press enter to continue")

# ~ # account.tax fields to copy from source to target BROKEN
# ~ account_tax_fields = ['name', 'amount', 'sequence', 'description']
# ~ account_tax_unique = 'name'
# ~ # migrate_model('account.tax', migrate_fields = account_tax_fields, include=True, unique = account_tax_unique)

if debug:
    input("press enter to continue")

# res.groups fields to copy from source to target WORKING
migrate_model('res.groups', include=False, create=False)

if debug:
    input("press enter to continue")

# product.public.category fields to copy from source to target WORKING
migrate_model('product.public.category', include=False, create=False)

if debug:
    input("press enter to continue")

# product.attribute fields to copy from source to target WORKING
product_attribute_custom = {'type': 'display_type'} # create variant should be hardcoded to no_variant
product_attribute_hard_code = {'create_variant': 'always'}
migrate_model('product.attribute', include=False, create=False, custom = product_attribute_custom, hard_code = product_attribute_hard_code)

if debug:
    input("press enter to continue")


# product.attribute.value fields to copy from source to target WORKING
migrate_model('product.attribute.value', include=False, create=False)

if debug:
    input("press enter to continue")

# product.category fields to copy from source to target
product_category_hard_code = {
    'property_cost_method': 'standard',
    'property_valuation': 'manual_periodic'
}
migrate_model('product.category', include=False, create=False, hard_code = product_category_hard_code)

if debug:
    input("press enter to continue")

# product.template fields to copy from source to target NEEDS uom.uom to be migrated, which is product.uom on odoo8
product_template_custom = {
    'image_medium' : 'image_1920',
}
# ~ migrate_model('product.template', migrate_fields = product_template_fields, include=True, custom = product_template_custom) #the old one had some weird checks for default code? incase it doesnt work

# product.product fields to copy from source to target
product_product_custom = {
    'image' : 'image_1920'
}
# ~ migrate_model('product.product', migrate_fields = product_product_fields, include=True, custom = product_product_custom)
#
# if default_variant_ids:
#     target.env['product.product'].browse(default_variant_ids).unlink()








