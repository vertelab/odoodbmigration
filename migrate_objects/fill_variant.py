	#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = False

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
product_product_domain = [('access_group_ids', '=', 286), ('sale_ok', '=', True), ('website_published', '=', True)]
#product_product_domain = [('id', 'in', [2112])]
product_product_exclude = ['image','uom_po_id','message_follower_ids', 'company_id', 'attribute_value_names', 'product_variant_ids', 'virtual_available_days', 'purchase_line_warn', 'purchase_line_warn_message', 'uom_id', 'sale_line_warn', 'categ_id', 'access_group_ids', 'product_tmpl_id', 'inventory_availability']
product_product_custom = {
    'public_desc': 'description_webshop',
    'use_desc': 'description_use',
    'ingredients': 'description_ingredients',
    'accessory_product_ids': 'variant_accessory_product_ids',
}
product_product_hardcode = {'type': 'product', 'company_id': 1}
product_product_calc = {'lst_price': """
try:
   p_pl_v_id = source.env['product.pricelist.version'].search_read([('pricelist_id', '=', 1)], ['id'], order='date_end desc', limit=1)[0]['id']
   p_pl_i_price = source.env['product.pricelist.item'].search_read([('product_id', '=', r), ('price_version_id', '=', p_pl_v_id)], ['price_surcharge'], limit=1)[0]['price_surcharge']
   pricelist_item_fields = {
   'product_id': get_target_id_from_id('product.product', r),
   'compute_price': 'fixed',
   'name': record['name'],
   'fixed_price': p_pl_i_price,
   'min_quantity': 0,
   'pricelist_id': 1,
   'applied_on': '0_product_variant',
   'company_id': 1,
   }
   custom_xml = 'variant_price_'
   if not create_record_and_xml_id('product.pricelist.item', 'product.pricelist.item', pricelist_item_fields, r, custom_xml_id = custom_xml):
      get_target_record_from_id('product.pricelist.item', custom_xml+str(r)).write(pricelist_item_fields)
      print(f"Writing to existing {pricelist_item_fields}")
except:
   pass
"""}
migrate_model('product.product', include=False, custom=product_product_custom, domain=product_product_domain, migrate_fields=product_product_exclude, hard_code=product_product_hardcode, create=False, calc=product_product_calc)
if debug:
    input("press enter to continue")


