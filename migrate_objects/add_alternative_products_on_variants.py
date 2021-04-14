#!/usr/bin/env python3
from configuration import *


for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, ['id', 'alternative_product_ids'])
    target_product = get_target_record_from_id('product.product', source_product_id)
    if not target_product:
    	continue
    try: 
    	alternative_products_to_write = [ get_target_record_from_id('product.template', group).id for group in source_product['alternative_product_ids'] ]
    except:
    	continue

    print("target template:", target_product, flush=True)
    print("group id in target db:", alternative_products_to_write, flush=True)

    target_product.alternative_product_ids = [(6, 0, alternative_products_to_write)]
    
    print('added', target_product.alternative_product_ids,'as alternative product of', target_product.id)
