#!/usr/bin/env python3

from configuration import *

for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_template_id, ['id', 'accessory_product_id'])
    target_product = get_target_record_from_id('product.product', source_product['id'])
    
    if not target_product:
        continue
    
    target_accessory_ids = [ get_target_record_from_id('product.product', access_id).id for access_id in source_product['accessory_product_id'] ] 
    target_accessory.accessory_product_id = [(6, 0, target_accessorry_ids)]

    print("wrote accessory_product_id to", target_product.id)

