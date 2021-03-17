#!/usr/bin/env python3

from configuration import *

for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, ['id', 'group_ids'])
    target_category = get_target_record_from_id('product.public.category', source_category['id'])

    if not target_category:
        continue
    
    group_to_write = [ get_target_record_from_id('res.groups', group).id for group in source_category['group_ids'] ]

    print("target category:", target_category, flush=True)
    print("group id in target db:", group_to_write, flush=True)

    target_category.access_group_ids = [(6, 0, group_to_write)]
    
    print('added', target_category.access_group_ids,'as access group of', target_category.id)
