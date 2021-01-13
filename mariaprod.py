# import argparse
# import json
# import logging
# import sys
# try:
#     import odoorpc
# except ImportError:
#     raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')
# #%% ---------------------------------------------------------------------------

# source_params = {
#             "host" : "localhost",
#             "port" : 5080,
#             "db"   : "dermanord",
#             "user" : "admin",
#             "password"  : "InwX11Je3DtifHHb"        
#         }

# target_params = {
#             "host" : "81.170.214.150",
#             "port" : 8069,
#             "db"   : "maria_demo",
#             "user" : "admin",
#             "password"  : "PVLd2bXhfLHeqGir"        
#         }

# fields = [
#               'active','description','description_sale',
#               'default_code','name','list_price',
#               'standard_price',
#               'website_description',
#               'website_published']

# # nfields = fields + ['old_id']

# source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
# source.login(source_params["db"],login=source_params["user"],password=source_params["password"])
# target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
# target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

# parents=[]
# print('hej')
# # for target_id in target.env['product.template'].search([]):
# #   target_product = target.env['product.template'].browse(target_id)
#   # target_product.unlink()


# # target_product = target.env['product.template'].create({'name': 'sandra'})
# # print(target_product)

# for source_id in source.env['product.product'].search([]):
#   print ('hej')
#   source_product = source.env['product.product'].read(source_id, fields)
#   target_product = target.env['product.product'].create({key:source_product[key] for key in fields})
#   # target_product = target.env['product.template'].create({key:source_product[key] for key in fields})
#   # target_product.old_id = source_id



import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')
#%% ---------------------------------------------------------------------------

source_params = {
            "host" : "localhost",
            "port" : 5080,
            "db"   : "dermanord",
            "user" : "admin",
            "password"  : "InwX11Je3DtifHHb"        
        }

target_params = {
            "host" : "81.170.214.150",
            "port" : 8069,
            "db"   : "maria_demo",
            "user" : "admin",
            "password"  : "PVLd2bXhfLHeqGir"        
        }


fields = [
              'name','list_price']

# fields = [
#               'active','description','description_sale','image',
#               'default_code','name','list_price',
#               'standard_price',
#               'website_description',
#               'website_published','public_desc', 'reseller_desc']

# nfields = fields + ['old_id']

source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])
target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

parents=[]
print('hej')
# for target_id in target.env['product.template'].search([]):
#   target_product = target.env['product.template'].browse(target_id)
  # target_product.unlink()


# target_product = target.env['product.template'].create({'name': 'sandra'})
# print(target_product)

for source_id in source.env['product.template'].search([]):
  print ('hej')
  # source_product = source.env['product.template'].read(source_id, fields)
  # target_product = target.env['product.template'].create({key:source_product[key] for key in fields})
  target_product.image_1920 = source_id.mapped('image_medium')

  target.env['product.template'].write(target_product, {'image_1920': source_product['image_medium']})
  # target_product = target.env['product.template'].create({key:source_product[key] for key in fields})
  # target_product.old_id = source_id
