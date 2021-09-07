#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

# to force all objects of a model to go through data updating(to for example add new fields that gets migrated) run the following sql command: 
# UPDATE table_name SET last_migration_date = NULL;

debug = True

if debug:
    input("press enter to continue")

# ~ # product.product fields to copy from source to target WORKS
product_product_domain = [('id', '=', 2148)]
#product_product_include = ['image']
product_product_include = ['image', 'image_attachment_ids']
product_product_custom = {
    'image' : 'image_1920',
}
product_product_calc = {'image_attachment_ids': """
print("image_attachment_ids")
print(record['image_attachment_ids'])
for image_id in record['image_attachment_ids']:
    print(image_id)
    image = source.env['ir.attachment'].browse(image_id)
    print(image)
    if image.datas != record['image']:
        image_fields = {
            'image_1920': image.datas,
            'name': image.name,
            'product_variant_id': get_target_id_from_id('product.product', r),
            'sequence': image.sequence
        }
        print("#"*99)
        img = create_record_and_xml_id('product.image', 'ir.attachment', image_fields, image_id)
        print(img)
        if img:
            print("set operation")
            get_target_record_from_id('product.product', str(r)).write({'product_variant_image_ids': [(4, get_target_id_from_id('product.image', image_id), 0)]})
        if not img:
            get_target_record_from_id('product.image', image_id).write(image_fields)
            print(f"Writing to existing {image_fields}")
        print("#"*99)
"""}

migrate_model('product.product', include=True, calc=product_product_calc, custom=product_product_custom, migrate_fields=product_product_include, domain=product_product_domain, create=False)
#migrate_model('product.product', include=True, calc=product_product_calc, domain=product_product_domain, custom=product_product_custom, migrate_fields=product_product_include, create=False)
#migrate_model('product.template', include=True, custom=product_product_custom, migrate_fields=product_product_include, create=False)
if debug:
    input("press enter to continue")




