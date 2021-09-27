#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

if debug:
    input("press enter to continue")

# product.template fields to copy from source to target WORKS(needs uom to be set up correctly)
product_template_exclude = ['message_follower_ids', 'company_id', 'product_variant_ids', 'product_variant_count', 'variant_access_group_ids', 'image', 'public_categ_ids']
product_template_custom = {}
product_template_hardcode = {
     'company_id': 1,
     'inventory_availability': 'never',
}
#product_template_domain = [('access_group_ids', '=', 286), ('sale_ok', '=', True), ('website_published', '=', True)]
product_template_domain = [('id', 'in', [2338])]
migrate_model('product.template', include=False, domain = product_template_domain, custom=product_template_custom, migrate_fields = product_template_exclude, hard_code = product_template_hardcode, create = False)

if debug:
    input("press enter to continue")





