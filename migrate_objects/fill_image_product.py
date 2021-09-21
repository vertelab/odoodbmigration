#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = False

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
#product_product_domain = [('id', 'in', [2921,3232,5540,9796,9799])]
product_product_domain = [('access_group_ids', '=', 286), ('sale_ok', '=', True), ('website_published', '=', True)]
#product_product_include = ['image']
product_product_include = ['image', 'default_code']
product_product_custom = {
    'image' : 'image_1920',
}

#migrate_model('product.product', include=True, calc=product_product_calc, custom=product_product_custom, migrate_fields=product_product_include, domain=product_product_domain, create=False)
#migrate_model('product.product', include=True, calc=product_product_calc, domain=product_product_domain, custom=product_product_custom, migrate_fields=product_product_include, create=False)
migrate_model('product.template', include=True, migrate_fields=product_product_include, custom=product_product_custom, domain=product_product_domain, create=False)
if debug:
    input("press enter to continue")




