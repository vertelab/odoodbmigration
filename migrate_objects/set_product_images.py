#!/usr/bin/env python3

from configuration import *

# source : target
# image -> image_1920
# image_medium -> image_1024
# image_small -> image_512

for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, ['image', 'image_medium', 'image_small'])
    target_product = get_target_record_from_id('product.product', source_product_id)
    target_product.write({'image_1920' : source_product['image'], 'image_1024' : source_product['image_medium'], 'image_512', source_product['image_small']})
    print("DONE", target_product.id)
