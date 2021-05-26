from configuration import *

# ---------------------------------------------------------------------------
# this code replaces res.company at target with source, res.company
# ---------------------------------------------------------------------------
model = 'res.company'
res_company = source.env[model].browse(1)
fields = get_all_fields(model, exclude=['partner_id', 'user_ids'])
vals = source.env[model].read(1, fields)
vals.update({'country_id': get_id_from_xml_id(res_company.country_id)})
vals.update({'currency_id': get_id_from_xml_id(res_company.currency_id)})
vals.update({'paperformat_id': target.env.ref('base.paperformat_euro').id})
target.env[model].browse(1).write(vals)

# ---------------------------------------------------------------------------
# WORKS!
# ---------------------------------------------------------------------------
migrate_model('res.partner',
              exclude=['message_follower_ids', 'user_ids'])

migrate_model('account.account.type',
              custom={'internal_group': 'equity'})

migrate_model('account.tax')

migrate_model('crm.lead',
              exclude=['message_follower_ids'])

migrate_model('ir.attachment',
              diff={'datas_big': 'datas'},
              custom={'public': True})

migrate_model('ir.config_parameter',
              exclude=['name'])

migrate_model('product.pricelist')

migrate_model('product.template',
              exclude=[
                  'message_follower_ids', 'taxes_id', 'supplier_taxes_id'])

migrate_model('product.product',
              exclude=[
                  'message_follower_ids', 'taxes_id', 'supplier_taxes_id'])

migrate_model('sale.order',
              exclude=['message_follower_ids'])

# ---------------------------------------------------------------------------
# PROBLEM!
# ---------------------------------------------------------------------------
# ==> 'code': 'b0' <==
# migrate_model('account.account',
#               diff={'user_type': 'user_type_id'})
