#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

debug = True

# project.project fields to copy from source to target WORKS
project_project_fields = ['name', 'alias_contact', 'alias_defaults', 'alias_id', 'alias_model_id', 'company_id']
project_project_hard_code = {
    'rating_status': 'stage',
    'rating_status_period': 'weekly',
    'privacy_visibility': 'followers'
}
migrate_model('project.project', migrate_fields = project_project_fields, include=True, hard_code = project_project_hard_code)


if debug:
    input("press enter to continue")

# project.task fields to copy from source to target WORKS
project_task_fields = ['company_id', 'kanban_state', 'name']
project_task_hard_code = {

}
migrate_model('project.task', migrate_fields = project_task_fields, include=True, hard_code = project_task_hard_code)


if debug:
    input("press enter to continue")

# ~ # res.partner fields to copy from source to target WORKS
res_partner_fields = ['name', 'email', 'mobile', 'phone', 'street', 'city', 'zip']

# ~ # this domain will migrate all users in a specified group
# ~ # res_partner_domain = [('partner_id.commercial_partner_id.access_group_ids', '=', target.env.ref("__export__.res_groups_283").id)]

# ~ # this domain will migrate users with the specified ids
res_partner_ids = []
res_partner_domain = [('id', '=', id) for id in res_partner_ids]
migrate_model('res.partner', migrate_fields= res_partner_fields, include=True, domain = res_partner_domain)


if debug:
    input("press enter to continue")

# res.partner.bank fields to copy from source to target BROKEN
res_partner_bank_fields = ['acc_number', 'partner_id']
migrate_model('res.partner.bank', migrate_fields= res_partner_bank_fields, include=True, unique = ['acc_number'])

if debug:
    input("press enter to continue")

# hr.employee fields to copy from source to target WORKS
hr_employee_fields = ['name', 'work_email', 'mobile_phone', 'work_location', 'company_id']
hr_employee_custom = {
    'image_medium' : 'image_1920',
}
migrate_model('hr.employee', migrate_fields = hr_employee_fields, include=True, custom=hr_employee_custom)

if debug:
    input("press enter to continue")

# hr.department fields to copy from source to target WORKS
hr_department_fields = ['name']
migrate_model('hr.department', migrate_fields = hr_department_fields, include=True)

if debug:
    input("press enter to continue")

# hr.attendance fields to copy from source to target WORKS
hr_attendance_fields = ['name', 'work_email', 'mobile_phone', 'work_location', 'company_id']
hr_attendance_custom = {
    'image_medium' : 'image_1920',
}
# ~ # migrate_model('hr.attendance', migrate_fields = hr_employee_fields, include=True, custom=hr_employee_custom)

if debug:
    input("press enter to continue")

# account.account.type fields to copy from source to target WORKING
account_type_field = ['name']
account_type_hard_code = {'type': 'receivable', 'internal_group': 'equity'}
migrate_model('account.account.type', migrate_fields = account_type_field, include=True, hard_code = account_type_hard_code)

if debug:
    input("press enter to continue")

# account.account fields to copy from source to target WORKING
account_fields = ['code', 'name', 'company_id']
account_custom = {'user_type': 'user_type_id'}
account_hard_code = {'reconcile': 1}
account_unique = ['code']
migrate_model('account.account', migrate_fields = account_fields, hard_code = account_hard_code, include=True, custom = account_custom, unique = account_unique)

if debug:
    input("press enter to continue")

# account.journal fields to copy from source to target WORKING
account_journal_fields = ['code', 'name', 'company_id', 'type']
account_journal_custom = {}
account_journal_hard_code = {'invoice_reference_model': 'odoo', 'invoice_reference_type': 'partner'}
account_journal_unique = ['code']
migrate_model('account.journal', migrate_fields = account_journal_fields, hard_code = account_journal_hard_code, include=True, custom = account_journal_custom, unique = account_journal_unique)

if debug:
    input("press enter to continue")

# account.move fields to copy from source to target WORKING
account_move_fields = ['date', 'name', 'journal_id']
account_move_custom = {}
account_move_hard_code = {'move_type': 'entry'}
account_move_unique = ['name']
account_move_calc = {'currency_id': r" return source.env['account.move'].search_read(record['journal_id'], 'currency')"}
# ~ #migrate_model('account.move', migrate_fields = account_move_fields, hard_code = account_move_hard_code, include=True, custom = account_move_custom, unique = account_move_unique)

if debug:
    input("press enter to continue")

# account.invoice fields to copy from source to target BROKEN
account_invoice_fields = ['name', 'journal_id']
account_invoice_custom = {
    'type': 'move_type',
    'date_invoice': 'date'
    }
account_invoice_unique = ['name']
account_invoice_calc = {}
account_invoice_xml_id_suffix = 'b'
# ~ #migrate_model({'account.invoice': 'account.move'}, migrate_fields = account_invoice_fields, include=True, custom = account_invoice_custom, unique = account_invoice_unique, xml_id_suffix = account_invoice_xml_id_suffix)

if debug:
    input("press enter to continue")

# ~ # res.users fields to copy from source to target WORKS
res_users_fields = ['company_id', 'login', 'partner_id']
res_users_custom = {
    'property_account_payable': 'property_account_payable_id',
    'property_account_receivable': 'property_account_receivable_id'
}
res_users_hard_code = {
    'notification_type': 'email'
}
res_users_ids = []
res_users_domain = [('id', '=', id) for id in res_users_ids]
res_users_unique = ['login']
migrate_model('res.users', migrate_fields = res_users_fields, include=True, custom=res_users_custom, hard_code=res_users_hard_code, unique=res_users_unique, domain = res_users_domain)

if debug:
    input("press enter to continue")

# product.pricelist fields to copy from source to target WORKING
product_pricelist_fields = ['name', 'code', 'display_name']
migrate_model('product.pricelist',migrate_fields = product_pricelist_fields, include=True, )

if debug:
    input("press enter to continue")

# ~ # product.pricelist.item fields to copy from source to target WORKING
product_pricelist_item_fields = ['price_discount', 'price_round', 'price_discount', 'price_min_margin', 'price_max_margin']
migrate_model('product.pricelist.item', migrate_fields = product_pricelist_item_fields , include=True, )

if debug:
    input("press enter to continue")

# res.currency fields to copy from source to target WORKING i think?
res_currency_fields = ['name', 'symbol']
res_currency_unique = ['name']
migrate_model('res.currency', migrate_fields = res_currency_fields, include=True, unique = res_currency_unique)

if debug:
    input("press enter to continue")

# stock.location fields to copy from source to target WORKING
stock_location_fields = ['name', 'usage']
migrate_model('stock.location', migrate_fields = stock_location_fields, include=True, )

if debug:
    input("press enter to continue")

# stock.warehouse fields to copy from source to target WORKING
stock_warehouse_fields = ['name', 'code', 'view_location_id', 'delivery_steps', 'reception_steps', 'partner_id', 'lot_stock_id', 'view_location_id']
stock_warehouse_unique = ['code']
migrate_model('stock.warehouse', migrate_fields = stock_warehouse_fields, include=True, unique = stock_warehouse_unique)

if debug:
    input("press enter to continue")

# sale.order fields to copy from source to target WORKING
sale_order_fields = ['name', 'date_order', 'company_id', 'partner_id', 'partner_shipping_id', 'partner_invoice_id', 'picking_policy', 'pricelist_id', 'warehouse_id']
migrate_model('sale.order', migrate_fields = sale_order_fields, include=True, )

if debug:
    input("press enter to continue")

# sale.order.line fields to copy from source to target WORKING
sale_order_line_fields = ['name', 'price_unit', 'product_uom_qty', 'order_id', 'company_id']
account_custom = {
    'delay': 'customer_lead'
}
migrate_model('sale.order.line', migrate_fields = sale_order_line_fields, include=True, custom = account_custom, hard_code = {'product_id': 45})

if debug:
    input("press enter to continue")

# res.groups fields to copy from source to target NOT WORKING(cant migrate groups from 8, they work differently)
# ~ res_groups_fields = ['name']
# ~ res_groups_unique = ['name']
# ~ migrate_model('res.groups', migrate_fields = res_groups_fields, include=True, unique = res_groups_unique, just_bind = True)

if debug:
    input("press enter to continue")

# ~ # product.public.category fields to copy from source to target WORKING
product_public_category_fields = ['name', 'display_name']
migrate_model('product.public.category', migrate_fields = product_public_category_fields, include=True, )

if debug:
    input("press enter to continue")

# product.attribute fields to copy from source to target WORKING
product_attribute_fields = ['name']
product_attribute_custom = {'type': 'display_type'} # create variant should be hardcoded to no_variant
product_attribute_hard_code = {'create_variant': 'always'}
migrate_model('product.attribute', migrate_fields = product_attribute_fields, include=True, custom = product_attribute_custom, hard_code = product_attribute_hard_code)

if debug:
    input("press enter to continue")


# product.attribute.value fields to copy from source to target WORKING
product_attribute_value_fields = ['name', 'attribute_id']
product_attribute_value_unique = ['name', 'attribute_id']
migrate_model('product.attribute.value', migrate_fields = product_attribute_value_fields, include=True, unique = product_attribute_value_unique)

if debug:
    input("press enter to continue")

# ~ # product.category fields to copy from source to target
product_category_fields = ['name']
product_category_custom = {
}
product_category_hard_code = {
    'property_cost_method': 'standard',
    'property_valuation': 'manual_periodic'
}
migrate_model('product.category', migrate_fields = product_category_fields, include=True, hard_code = product_category_hard_code)

if debug:
    input("press enter to continue")

# product.template fields to copy from source to target NEEDS uom.uom to be migrated, which is product.uom on odoo8
product_template_fields = ['name', 'sale_ok', 'purchase_ok', 'list_price', 'standard_price', 'description_sale', 'default_code', 'website_published', 'active', 'type', 'categ_id', 'sale_line_warn', ]
product_template_custom = {
    'image_medium' : 'image_1920',
}
# Not used?
migrate_model('product.template', migrate_fields=product_template_fields, include=True, custom=product_template_custom, after_migration=product_tmpl_set_attributes)
#the old one had some weird checks for default code? incase it doesnt work

# product.product fields to copy from source to target
product_product_fields = ['name', 'sale_ok', 'description', 'purchase_ok', 'list_price', 'description_sale', 'default_code', 'active',
'website_published', 'product_tmpl_id', 'lst_price', 'volume', 'standard_price', 'available_in_pos', 'weight',
'ingredients', 'ingredients_last_changed', 'ingredients_changed_by_uid', 'use_desc', 'use_desc_last_changed', 'use_desc_changed_by_uid', 'event_ok']
product_product_custom = {
    'image' : 'image_1920'
}
migrate_model('product.product', migrate_fields=product_product_fields, include=True, custom=product_product_custom)

# ~ if default_variant_ids:
    # ~ target.env['product.product'].browse(default_variant_ids).unlink()
