#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

debug = True

if debug:
    input("press enter to continue")

# product.template fields to copy from source to target NEEDS uom.uom to be migrated, which is product.uom on odoo8
product_template_fields = ['name', 'sale_ok', 'purchase_ok', 'list_price', 'standard_price', 'description_sale', 'default_code', 'website_published', 'active', 'type', 'categ_id', 'sale_line_warn', ]
product_template_custom = {
    'image' : 'image_1920',
}
product_template_hardcode = {'company_id': 1}
product_template_domain = [('access_group_ids', '=', 286), ('sale_ok', '=', True), ('website_published', '=', True)]
#product_template_domain = [('id', 'in', ['10408', '10407'])]
migrate_model('product.template', hard_code = product_template_hardcode, migrate_fields=product_template_fields, include=True, custom=product_template_custom, after_migration=product_tmpl_set_attributes, domain=product_template_domain)
#the old one had some weird checks for default code? incase it doesnt work

# product.product fields to copy from source to target
product_product_fields = ['name', 'sale_ok', 'description', 'purchase_ok', 'list_price', 'description_sale', 'default_code', 'active', 'website_published', 'product_tmpl_id', 'lst_price', 'volume', 'standard_price', 'weight']
product_product_custom = {
    'image' : 'image_1920'
}
#migrate_model('product.product', hard_code = product_template_hardcode, migrate_fields=product_product_fields, include=True, custom=product_product_custom, domain=product_template_domain)

