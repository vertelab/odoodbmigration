from configuration import *

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, ['id', 'access_group_ids'])
    target_template = get_target_record_from_id('product.template', source_template_id)
    
    groups_to_write = [ get_target_record_from_id('res.groups', group).id for group in source_template['access_group_ids'] ]

    print("target template:", target_template, flush=True)
    print("group id in target db:", groups_to_write, flush=True)

    target_template.access_group_ids = [(6, 0, groups_to_write)]
    
    print('added', target_template.access_group_ids,'as access group of', target_template.id)

for source_product_id in source.env['product.product'].search([]):
    source_product = source.env['product.product'].read(source_product_id, ['id', 'access_group_ids'])
    target_product = get_target_record_from_id('product.product', source_product_id)
    
    group_to_write = [ get_target_record_from_id('res.groups', group).id for group in source_product['access_group_ids'] ]

    print("target template:", target_product, flush=True)
    print("group id in target db:", group_to_write, flush=True)

    target_product.access_group_ids = [(6, 0, group_to_write)]
    
    print('added', target_product.access_group_ids,'as access group of', target_product.id)
