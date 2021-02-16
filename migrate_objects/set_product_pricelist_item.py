#!/usr/bin/env python3

from configuration import *

for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, ['id', 'product_id', 'base_pricelist_id', 'price_max_margin', 'price_min_margin', 'price_round', 'price_discount', 'price_surcharge', 'min_quantity', ])
    
    try:
        target_pricelist_item = get_target_record_from_id('product.pricelist.item', source_pricelist_item_id)
        target_pricelist_product_id = get_target_record_from_id('product.product', source_pricelist_item['product_id'][0]) or False
        target_pricelist_item_pricelist_id = get_target_record_from_id('product.pricelist', source_pricelist_item['base_pricelist_id'][0])
        
        target_pricelist_item.price_max_margin = source_pricelist_item['price_max_margin']  
        target_pricelist_item.price_min_margin = source_pricelist_item['price_min_margin']
        target_pricelist_item.price_round = source_pricelist_item['price_round']
        target_pricelist_item.price_discount = source_pricelist_item['price_discount']
        target_pricelist_item.price_surcharge = source_pricelist_item['price_surcharge']
        
        target_pricelist_item.compute_price = "formula"
        target_pricelist_item.base = "pricelist"
        target_pricelist_item.applied_on = "0_product_variant"
        
        if target_pricelist_product_id:
            target_pricelist_item.product_id = target_pricelist_product_id
        
        target_pricelist_item.pricelist_id = target_pricelist_item_pricelist_id
        
        print("OK", source_pricelist_item)
    except:
        print("FAULTY", source_pricelist_item)

    print()

