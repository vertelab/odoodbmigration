#!/usr/bin/env python3

from configuration import *

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, ['id', 'product_variant_ids'])
    target_template = get_target_record_from_id('product.template', source_template_id)
    
    variants_to_write = [ get_target_record_from_id('product.product', variant).id for variant in source_template['product_variant_ids'] ]

    print("target template:", target_template, flush=True)
    print("variants id in target db:", variants_to_write, flush=True)

    target_template.product_variant_ids = [(6, 0, variants_to_write)]
    
    print('added', target_template.product_variant_ids,'as variants of', target_template.id)
