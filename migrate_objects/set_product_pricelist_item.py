#!/usr/bin/env python3

import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

from configuration import *

for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, ['id', 'product_id'])
    target_pricelist_item = get_target_record_from_id('product.pricelist.item', source_pricelist_item_id)
    
    if not target_pricelist_item:
        print("pricelist item not found in target")
        continue
    
    if not source_pricelist_item['product_id']:
        print("pricelist has no product?")
        continue
    
    target_pricelist_product = get_target_record_from_id('product.product', source_pricelist_item['product_id'][0])
    
    if not target_pricelist_product:
        print("product not found in target")
        continue
    
    target_pricelist_item.write({'product_id' : target_pricelist_product.id})
    
    print("wrote pricelist to product")
    
