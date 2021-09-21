#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

if debug:
    input("press enter to continue")

# ~ # res.partner fields to copy from source to target WORKS
res_partner_domain = [('id', 'in', [5522])]
res_partner_exclude = ['invoice_ids', 'message_follower_ids', 'access_group_ids', 'user_ids', 'lang']
res_partner_calc = {'type': """
type_val = record['type']
if type_val == 'default':
    type_val = 'contact'
vals[key] = type_val
"""}
res_partner_custom = {
    'agents': 'agent_ids'
}
res_partner_hard_code = {
    'property_product_pricelist': 1,
    'company_id': 1,
}
migrate_model('res.partner', migrate_fields=res_partner_exclude, include=False, create=False, calc=res_partner_calc, domain=res_partner_domain, custom=res_partner_custom, hard_code=res_partner_hard_code)


if debug:
    input("press enter to continue")




