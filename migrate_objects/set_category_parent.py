#!/usr/bin/env python3

from configuration import *
    
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, ['id', 'parent_id'])
    source_category_parent_id = None if not source_category['parent_id'] else source_category['parent_id'][0]
    
    target_category = get_target_record_from_id('product.public.category', source_category['id'])
    
    if source_category_parent_id:
        target_parent_category_id = get_target_record_from_id('product.public.category', source_category_parent_id).id
        target_category.write({ 'parent_id' : target_parent_category_id })
        print("wrote", target_parent_category_id, "to parent_id of", target_category)
    else:
        print(target_category, "has no parent")
