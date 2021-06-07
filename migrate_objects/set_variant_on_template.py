#!/usr/bin/env python3

from configuration import *

t2s_attr_values = {}
for data in target.env['ir.model.data'].search_read([
        ('model', '=', 'product.attribute.value'),
        ('name', '=like', 'product_attribute_value_%'),
        ('module', '=', '__import__')], ['res_id', 'name']):
    t2s_attr_values[data['res_id']] = int(data['name'].replace('product_attribute_value_', ''))

for source_template_id in source.env['product.template'].search([('id', '=', 4838)]):
    target_template = get_target_record_from_id('product.template', source_template_id)
    target_lines = target.env['product.template.attribute.line'].search_read([('product_tmpl_id', '=', target_template.id)], ['attribute_id', 'value_ids'])
    for line in source.env['product.attribute.line'].search_read([('product_tmpl_id', '=', source_template_id)], ['attribute_id', 'value_ids']):
        target_attr_id = get_target_record_from_id('product.attribute', line['attribute_id'][0]).id
        target_val_ids = []
        for id in line['value_ids']:
            target_val_ids.append(get_target_record_from_id('product.attribute.value', id).id)
        target_line = [l for l in filter(lambda r: r['attribute_id'][0] == target_attr_id, target_lines)]
        target_line = target_line and target_line[0] or None
        if target_line:
            if set(target_val_ids) == set(target_line['value_ids']):
                # Source and target lines are identical
                continue
            # This will create/delete/archive product variants
            target.env['product.template.attribute.line'].write(target_line['id'], {'value_ids': [(6, 0, target_val_ids)]})
        else:
            # This will create/delete/archive product variants
            target.env['product.template.attribute.line'].create({
                'product_tmpl_id': target_template.id,
                'attribute_id': target_attr_id,
                'value_ids': [(6, 0, target_val_ids)],
            })
        for variant in target.env['product.product'].search_read([('product_tmpl_id', '=', target_template.id)], ['active']):
            source_variant_id = False # do search with attribute values
            product_template_attribute_value_ids
            value_ids = []
            for vline in target.env['product.template.attribute.value'].search_read(
                    [('ptav_product_variant_ids', '=', variant['id'])],
                    ['product_attribute_value_id']):
                value_ids.append(t2s_attr_values[vline[['product_attribute_value_id']]])
            domain = [('attribute_value_ids', '=', id) for id in value_ids]
            domain.append(('product_tmpl_id', '=', source_template_id))
            source_variant = source['product.product'].search_read(domain, ['active'])
            source_variant = source_variant and source_variant[0] or None
            if source_variant_id:
                create_xml_id('product.product', variant['id'], source_variant['id'])
                if not source_variant['active'] and variant['active']:
                    target.env['product.product'].write(variant['id'], {'active': False})
            else:
                # Newly created in target. Make inactive.
                target.env['product.product'].write(variant['id'], {'active': False})

# ~ for source_product_id in source.env['product.product'].search([]):
    # ~ source_product = source.env['product.product'].read(source_product_id, ['id', 'alternative_product_ids', 'optional_product_ids'])
    # ~ target_product = get_target_record_from_id('product.product', source_product['id'])
    
    # ~ if not target_product:
        # ~ continue
    
    # ~ target_alt_prod_ids = [ get_target_record_from_id('product.template', alt_prod_id).id for alt_prod_id in source_product['alternative_product_ids', 'optional_product_ids']]
    # ~ target_product.alternative_product_ids = [(6, 0, target_alt_prod_ids)]
    # ~ target_product.optional_product_ids = [(6, 0, target_alt_prod_ids)]

    # ~ print("wrote alternative_product_ids to", target_product.id)


