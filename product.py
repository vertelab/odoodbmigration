from configuration import *

all_module = source.env['ir.module.module'].search_read(
    [], ['name', 'dependencies_id'], order='name')
all_module_dependency = source.env['ir.module.module.dependency'].search_read(
    [], ['name'])
all_module2 = {x['name']: {'dependencies': sorted(next(
    z['name'] for z in all_module_dependency if z['id'] == y) for y in x['dependencies_id'])} for x in all_module}
if source.version.startswith('12'):
    product_template_fields = sorted(
        source.env['product.template'].fields_get().keys())
    product_template_model_id = source.env['ir.model'].search(
        [('model', '=', 'product.template')])
    product_template_modules = source.env['ir.model'].read(
        product_template_model_id)[0]['modules'].split(', ')
    product_template_modules_dependencies = [
        x for x in product_template_modules]
"""
account.tax
mrp.bom
mrp.bom.line
product.template.attribute.line
product.public.category

product.category
product.pricelist
product.image
product.pricelist.item
product.packaging
product.supplierinfo
"""

"""
account_asset - Odoo Enterprise Edition
asset_category_id            - many2one - account.asset.category
deferred_revenue_category_id - many2one - account.asset.category

alan_customize - atharvasystem.com
hover_image      - binary
product_brand_id - many2one - product.brand

delivery_hs_code - Core Odoo 12 not ported
hs_code - char

account_intrastat - Odoo Enterprise Edition
intrastat_id - many2one - account.intrastat.code

product - Core Odoo 12 - field not used
item_ids - one2many - product.pricelist.item
rental - boolean

stock_account - Core Odoo 12 - field not used
property_cost_method - selection - moved to product.category

sale_product_configurator - installs when checking Settings > Sales > ProductCatalog > ProductConfigurator
optional_product_ids - many2many - product.template

website_sale - Core Odoo 12 - field name changed
product_image_ids - one2many - product.image

sale_subscription - Camptocamp
recurring_invoice - boolean
"""


migrate_model(
    'product.template',
    bypass_date=1,
    create=0,
    diff={
        'image': 'image_1920',
        'life_time': 'expiration_time',
        'product_image_ids': 'product_template_image_ids', # website_sale
        'split_method': 'split_method_landed_cost',
    },
    ids=[10953])
