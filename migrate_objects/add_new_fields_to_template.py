from configuration import *

product_fields = {
    'name' : 'name',
 }


for source_template_id in source.env['product.template'].search([]):
    source_template_product = source.env['product.template'].read(source_template_id, list(product_fields.keys()) + ['type'])
    fields = { product_fields[key] : source_template_product[key] for key in product_fields.keys() }

    fields.update({'type': 'product'})
    
    target_template = get_target_record_from_id('product.template', source_template_id)
    
    if target_template:
        target_template.write(fields)
        print("wrote fields to product.template")
    else:
        print("write error")

