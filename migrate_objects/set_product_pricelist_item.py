#!/usr/bin/env python3

import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

import configuration

for source_attribute_value_id in source.env['product.pricelist.item'].search([]):
    source_product_pricelist_item_product_id = source.env['product.pricelist.item'].read(source_attribute_value_id, ['id'])
    target_pricelist_item = get_target_record_from_id('product.pricelist.item', source_attribute_value_id)
    target_pricelist_item.write({'product_id' : get_target_record_from_id('product.product', product_pricelist_item_product_id['id']).id})
