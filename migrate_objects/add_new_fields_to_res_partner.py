#!/usr/bin/env python3

from configuration import *

partner_fields = {
    'comment' : 'comment',
 }

for source_partner_id in source.env['res.partner'].search([]):
    source_partner = source.env['res.partner'].read(source_partner_id, list(partner_fields.keys()) + ['parent_id', 'property_product_pricelist'])
    fields = { partner_fields[key] : source_partner[key] for key in partner_fields.keys() }
    fields.update({'parent_id': source_partner['parent_id']})
    
    target_partner = get_target_record_from_id('res.partner', source_partner_id)

    pricelist_to_write = [ get_target_record_from_id('product.pricelist', pricelist).id for pricelist in source_partner['property_product_pricelist'] ]

    target_partner.property_product_pricelist = [(6, 0, pricelist_to_write)]

    
    if target_partner:
        target_partner.write(fields)
        print("wrote fields to res.partner")
    else:
        print("write error")

