#!/usr/bin/env python3

from configuration import *

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, ['id', 'public_categ_ids'])
    target_template = get_target_record_from_id('product.template', source_template['id'])
    
    if not target_template:
        continue
    
    target_categ_ids = [ get_target_record_from_id('product.public.category', categ_id).id for categ_id in source_template['public_categ_ids'] ] 
    target_template.public_categ_ids = [(6, 0, target_categ_ids)]

    print("wrote public_categ_ids to", target_template.id)
