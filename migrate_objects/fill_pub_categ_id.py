#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
product_product_domain = [('id', '=', 11751)]
#product_product_include = ['image']
product_product_include = ['image']
product_product_custom = {
    'image' : 'image_1920',
}


migrate_model('product.template', include=True, custom=product_product_custom, migrate_fields=product_product_include, create=False)
#migrate_model('product.product', include=True, calc=product_product_calc, domain=product_product_domain, custom=product_product_custom, migrate_fields=product_product_include, create=False)
#migrate_model('product.template', include=True, custom=product_product_custom, migrate_fields=product_product_include, create=False)
if debug:
    input("press enter to continue")




