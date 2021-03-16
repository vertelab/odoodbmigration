from configuration import *

variant_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'active' : 'active',
    'website_published': 'website_published',
    'image': 'image_1920',
    'image_medium': 'image_1024',
    'image_small': 'image_512',
    'default_code' : 'default_code',
    'lst_price' : 'lst_price',
    'list_price': 'list_price',
    'volume' : 'volume',
    'available_in_pos' : 'available_in_pos',
    'weight' : 'weight',
    'ingredients': 'ingredients',
    'ingredients_last_changed': 'ingredients_last_changed',
    'ingredients_changed_by_uid':'ingredients_changed_by_uid',
    'use_desc': 'use_desc',
    'use_desc_last_changed': 'use_desc_last_changed',
    'use_desc_changed_by_uid': 'use_desc_changed_by_uid',
    'event_ok': 'event_ok',
    'standard_price': 'standard_price',
    'public_desc': 'public_desc',
    'public_desc_last_changed': 'public_desc_last_changed',
    'public_desc_changed_by_uid': 'public_desc_changed_by_uid',
 }

for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, list(variant_fields.keys()) + ['type'])
    fields = { variant_fields[key] : source_product[key] for key in variant_fields.keys() }
    fields.update({'type': source_product['type']})
    
    target_product = get_target_record_from_id('product.product', source_product_id)
    
    if target_product:
        target_product.write(fields)
        print("wrote fields to product.product")
    else:
        print("write error")

