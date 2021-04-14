#!/usr/bin/env python3

from configuration import *

for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, ['id', 'accessory_product_ids'])
    target_product = get_target_record_from_id('product.product', source_product_id)
    
    group_to_write = [ get_target_record_from_id('product.product', group).id for group in source_product['accessory_product_ids']]

    print("target template:", target_product, flush=True)
    print("group id in target db:", group_to_write, flush=True)

    target_product.accessory_product_ids = [(6, 0, group_to_write)]
    
    print('added', target_product.accessory_product_ids,'as access group of', target_product.id)
