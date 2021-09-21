#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

debug = True


if debug:
    input("press enter to continue")

# ~ # res.partner fields to copy from source to target WORKS
res_partner_fields = ['name', 'email', 'mobile', 'phone', 'street', 'city', 'zip']

# ~ # this domain will migrate all users in a specified group
#res_partner_domain = [('partner_id.commercial_partner_id.access_group_ids', '=', target.env.ref("__export__.res_groups_283").id)]

# ~ # this domain will migrate users with the specified ids
#res_partner_ids = [29061]
res_partner_domain = [('id', 'in', [5522])]
migrate_model('res.partner', migrate_fields=res_partner_fields, include=True, domain=res_partner_domain)

if debug:
    input("press enter to continue")
