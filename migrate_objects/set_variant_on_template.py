#!/usr/bin/env python3

from configuration import *


for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, ['product_variant_ids'])
    target_template = get_target_record_from_id('product.template', source_template_id)
    
    print("source_template_id:", source_template_id)
    print("target_template_id:", target_template.id)
    
    variants_to_write = []
    for source_product_id in source_template['product_variant_ids']:
        target_product = get_target_record_from_id('product.product', source_product_id)

        if target_product:
            variants_to_write.append(target_product.id)
            
    print("writing variants:", variants_to_write)

    target_template.product_variant_ids = [(6, 0, variants_to_write)]

    print('added', target_template.product_variant_ids, 'as variants of', target_template.id)


for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, ['id', 'alternative_product_ids', 'optional_product_ids'])
    target_product = get_target_record_from_id('product.product', source_product['id'])
    
    if not target_product:
        continue
    
    target_alt_prod_ids = [ get_target_record_from_id('product.template', alt_prod_id).id for alt_prod_id in source_product['alternative_product_ids', 'optional_product_ids']]
    target_product.alternative_product_ids = [(6, 0, target_alt_prod_ids)]
    target_product.optional_product_ids = [(6, 0, target_alt_prod_ids)]

    print("wrote alternative_product_ids to", target_product.id)


