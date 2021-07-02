#!/usr/bin/env python3

from configuration import *

# Attribute values id translation, target to source
t2s_attr_values = {}

def get_t2s_attr_values():
    global t2s_attr_values
    if not t2s_attr_values:
        for data in target.env['ir.model.data'].search_read([
                ('model', '=', 'product.attribute.value'),
                ('name', '=like', 'product_attribute_value_%'),
                ('module', '=', IMPORT_MODULE_STRING)], ['res_id', 'name']):
            t2s_attr_values[data['res_id']] = int(data['name'].replace('product_attribute_value_', ''))
    return t2s_attr_values

# Migrate templates
def product_tmpl_set_attributes(source_template_id, target_template_id, create=False):
    print(f"product_tmpl_set_attributes: {source_template_id} {target_template_id}")
    target_lines = target.env['product.template.attribute.line'].search_read([('product_tmpl_id', '=', target_template_id)], ['attribute_id', 'value_ids'])
    attribute_line_ids = []
    updated_attr_line_ids = []
    values = {}
    for line in source.env['product.attribute.line'].search_read([('product_tmpl_id', '=', source_template_id)], ['attribute_id', 'value_ids']):
        target_attr_id = get_target_record_from_id('product.attribute', line['attribute_id'][0]).id
        target_val_ids = []
        for id in line['value_ids']:
            target_val_ids.append(get_target_record_from_id('product.attribute.value', id).id)
        target_line = [l for l in filter(lambda r: r['attribute_id'][0] == target_attr_id, target_lines)]
        target_line = target_line and target_line[0] or None
        if target_line and target_val_ids:
            target_lines.remove(target_line)
            if set(target_val_ids) == set(target_line['value_ids']):
                # Source and target lines are identical
                continue
            # This will create/delete/archive product variants
            attribute_line_ids.append((1, target_line['id'], {'value_ids': [(6, 0, target_val_ids)]}))
            #target.env['product.template.attribute.line'].write(target_line['id'], {'value_ids': [(6, 0, target_val_ids)]})
        elif target_val_ids:
            # This will create/delete/archive product variants
            attribute_line_ids.append((0, 0, {
                'product_tmpl_id': target_template_id,
                'attribute_id': target_attr_id,
                'value_ids': [(6, 0, target_val_ids)],
            }))
    # Check for removed attribute lines.
    for line in target_lines:
        attribute_line_ids.append((2, line['id']))
    if attribute_line_ids:
        values['attribute_line_ids'] = attribute_line_ids
    
    # Optional and Alternative products
    optional_product_ids = set()
    alternative_product_ids = set()
    for variant in source.env['product.product'].search_read([
            ('product_tmpl_id', '=', source_template_id)],
            ['id', 'optional_product_ids', 'alternative_product_ids']):
        # Not getting any optional products for some reason
        # ~ for tmpl_id in variant['optional_product_ids']:
            # ~ optional_product_ids.add(tmpl_id)
        for tmpl_id in variant['alternative_product_ids']:
            alternative_product_ids.add(tmpl_id)
    optional_product_ids = [get_target_record_from_id('product.template', tmpl_id) for tmpl_id in optional_product_ids]
    optional_product_ids = [r.id for r in optional_product_ids if r]
    alternative_product_ids = [get_target_record_from_id('product.template', tmpl_id) for tmpl_id in alternative_product_ids]
    alternative_product_ids = [r.id for r in alternative_product_ids if r]
    if optional_product_ids:
        values['optional_product_ids'] = optional_product_ids
    if alternative_product_ids:
        values['alternative_product_ids'] = alternative_product_ids
    
    # Write to template
    print(f"values: {values}")
    if values:
        target.env['product.template'].write(target_template_id, values)
    
    # Migrate Variant data
    for variant in target.env['product.product'].search_read([('product_tmpl_id', '=', target_template_id)], ['active']):
        # Match variants through attribute values
        'product_template_attribute_value_ids'
        # Translate target attribute value ids to source
        value_ids = []
        for vline in target.env['product.template.attribute.value'].search_read(
                [('ptav_product_variant_ids', '=', variant['id'])],
                ['product_attribute_value_id']):
            value_ids.append(get_t2s_attr_values()[vline['product_attribute_value_id'][0]])
        domain = [('attribute_value_ids', '=', id) for id in value_ids]
        domain.append(('product_tmpl_id', '=', source_template_id))
        
        source_variant = source.env['product.product'].search_read(domain, ['active'])
        source_variant = source_variant and source_variant[0] or None
        print(domain)
        print(source_variant)
        if source_variant:
            create_xml_id('product.product', variant['id'], source_variant['id'])
            if not source_variant['active'] and variant['active']:
                target.env['product.product'].write(variant['id'], {'active': False})
            elif source_variant['active'] and not variant['active']:
                target.env['product.product'].write(variant['id'], {'active': True})
        else:
            # Variant is auto-created, but doesn't exist in source. Make inactive.
            target.env['product.product'].write(variant['id'], {'active': False})
    if create:
        # Check for templates that use this template in Alternative or Optional products
        # Optional
        # ~ domain = [('module', '=', IMPORT_MODULE_STRING)]
        # ~ for id in source.env['product.template'].search([
                # ~ ('product_variant_ids.optional_product_ids', '=', source_template_id)]):
            # ~ domain.append(('name', '=', f"product_template_{id}"))
        # ~ if len(domain) > 1:
            # ~ target_tmpl_ids = [r['res_id'] for r in target.env['ir.model.data'].search_read(domain, ['res_id'])]
            # ~ if target_tmpl_ids:
                # ~ target.env['product.template'].write(
                    # ~ target_tmpl_ids,
                    # ~ {'optional_product_ids': [(4, target_template_id)]})
        # Alternative
        domain = [('module', '=', IMPORT_MODULE_STRING)]
        for id in source.env['product.template'].search([
                ('alternative_product_ids', '=', source_template_id)]):
            domain.append(('name', '=', f"product_template_{id}"))
        if len(domain) > 1:
            target_tmpl_ids = [r['res_id'] for r in target.env['ir.model.data'].search_read(domain, ['res_id'])]
            if target_tmpl_ids:
                target.env['product.template'].write(
                    target_tmpl_ids,
                    {'alternative_product_ids': [(4, target_template_id)]})
