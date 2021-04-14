#!/usr/bin/env python3

from configuration import *

for source_partner_id in source.env['res.partner'].search([]):
    source_partner = source.env['res.partner'].read(source_partner_id, ['id', 'access_group_ids'])
    target_partner = get_target_record_from_id('res.partner', source_partner['id'])

    if not target_partner:
        continue
    
    group_to_write = [ get_target_record_from_id('res.groups', group).id for group in source_partner['access_group_ids'] ]

    print("target template:", target_partner, flush=True)
    print("group id in target db:", group_to_write, flush=True)

    target_partner.access_group_ids = [(6, 0, group_to_write)]
    
    print('added', target_partner.access_group_ids,'as access group of', target_partner.id)