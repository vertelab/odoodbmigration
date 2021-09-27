#!/usr/bin/env python3

from configuration import *
from set_variant_on_template import *

debug = False

# ~ # account.journal fields to copy from source to target WORKING
account_journal_fields = ['code', 'name', 'type']
account_journal_custom = {}
account_journal_hard_code = {'invoice_reference_model': 'odoo', 'invoice_reference_type': 'partner', 'company_id':1}
account_journal_unique = ['code']
migrate_model('account.journal', migrate_fields = account_journal_fields, hard_code = account_journal_hard_code, include=True, custom = account_journal_custom, unique = account_journal_unique)

# ~ FIXA PERIODER
FIX PERIOD EXTERNAL ID 
source_to_target_dict = {
200:1,    #opening
201:2,    #01
202:3,    #02
203:4,    #03
204:5,    #04
205:6,    #05
206:7,    #06
207:8,    #07
208:9,    #08
209:10,    #09
210:11,   #10
211:12,    #11
212:13,    #12
}

for source_id in source_to_target_dict:
    target_id = source_to_target_dict[source_id]
    create_xml_id('account.period',target_id,source_id)
    
# account.move fields to copy from source to target WORKING
account_move_fields = ['date', 'name', 'journal_id', 'period_id', 'state', 'tax_amount',' credit', 'debit', 'balance', 'display_name', 'account_tax_id', 'ref','partner_id']
account_move_custom = {}
account_move_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
account_move_hard_code = {'move_type': 'entry'}
account_move_unique = ['name']
account_move_calc = {'currency_id': r" return source.env['account.move'].search_read(record['journal_id'], 'currency')"}
migrate_model('account.move', migrate_fields = account_move_fields, hard_code = account_move_hard_code, include=True, custom = account_move_custom, unique = account_move_unique,domain = account_move_domain)

# account.move.line fields to copy from source to target WORKING
account_move_line_fields = ['account_id', 'date', 'name', 'journal_id', 'move_id','credit','debit','display_name','account_tax_id','currency_id','partner_id']
account_move_line_custom = {"tax_code_id":"tax_line_id"}
account_move_line_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
account_move_hard_code = {'tax_id': 'tax_ids'}
account_move_unique = ['name']
account_move_line_calc = {'currency_id':r" return source.env['account.move.line'].search_read(record['journal_id'], 'currency')"}
migrate_model('account.move.line', migrate_fields = account_move_line_fields, include=True, custom = account_move_line_custom, unique = account_move_unique, domain = account_move_line_domain,calc = account_move_line_calc)


# ~ account_move_fields = ['name','state','ref']
# ~ account_move_custom = {}
# ~ account_move_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
# ~ account_move_unique = ['name']
# ~ migrate_model('account.move', migrate_fields = account_move_fields, include=True, unique = account_move_unique, domain = account_move_domain,create=False, bypass_date = True)

# ~ account_move_line_fields = []
# ~ account_move_line_custom = {"tax_code_id":"tax_line_id"}
# ~ account_move_line_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
# ~ #account_move_line_domain = [('move_id.name' ,'=',"145631")]
# ~ account_move_line_unique = ['name']
# ~ migrate_model('account.move.line', migrate_fields = account_move_line_fields, include=True, unique = account_move_line_unique, domain = account_move_line_domain,create=False, bypass_date = True, custom = account_move_line_custom)






# ~ # project.project fields to copy from source to target WORKS
# ~ project_project_fields = ['name', 'alias_contact', 'alias_defaults', 'alias_id', 'alias_model_id', 'company_id']
# ~ project_project_hard_code = {
    # ~ 'rating_status': 'stage',
    # ~ 'rating_status_period': 'weekly',
    # ~ 'privacy_visibility': 'followers'
# ~ }
# ~ migrate_model('project.project', migrate_fields = project_project_fields, include=True, hard_code = project_project_hard_code)


# ~ if debug:
    # ~ input("press enter to continue")

# ~ # project.task fields to copy from source to target WORKS
# ~ project_task_fields = ['company_id', 'kanban_state', 'name']
# ~ project_task_hard_code = {

# ~ }
# ~ migrate_model('project.task', migrate_fields = project_task_fields, include=True, hard_code = project_task_hard_code)


# ~ if debug:
    # ~ input("press enter to continue")

# res.partner fields to copy from source to target WORKS
# ~ res_partner_fields = ['name', 'email', 'mobile', 'phone', 'street', 'city', 'zip']

# this domain will migrate all users in a specified group
# res_partner_domain = [('partner_id.commercial_partner_id.access_group_ids', '=', target.env.ref("__export__.res_groups_283").id)]
# ~ res_partner_domain = [()]
# this domain will migrate users with the specified ids
# ~ res_partner_ids = ['15', '18', '21', '44', '67', '89', '101', '5412', '5474', '5481', '5522', '5684', '5760', '5853', '5919', '5990', '6158', '6406', '6453', '6560', '6770', '6804', '6845', '6846', '6848', '6851', '6860', '6864', '6865', '7010', '7027', '7053', '7058', '7061', '7102', '7139', '7152', '7185', '7222', '7230', '7413', '7527', '7733', '7781', '7801', '8127', '8134', '8296', '8426', '8477', '8594', '8688', '8760', '8773', '8775', '8777', '8779', '8805', '8811', '8897', '8947', '8957', '8969', '9033', '9034', '9064', '9080', '9091', '9101', '9133', '9160', '9175', '9182', '9216', '9235', '9273', '9287', '9303', '9304', '9308', '9313', '9321', '9323', '9331', '9338', '9374', '9404', '9534', '9586', '9631', '9639', '9665', '9704', '9705', '9713', '9714', '9755', '9801', '9815', '9821', '9837', '9853', '9858', '9860', '9867', '9888', '9907', '9910', '9914', '9979', '10026', '10080', '10088', '10090', '10103', '10127', '10129', '10167', '10456', '10470', '10834', '10859', '10869', '10873', '10877', '10891', '10926', '10927', '10950', '10953', '10970', '10978', '10993', '10996', '11024', '11029', '11032', '11055', '11071', '11073', '11078', '11081', '11115', '11116', '11117', '11146', '11150', '11161', '11178', '11181', '11185', '11201', '11207', '11212', '11239', '11243', '11249', '11275', '11276', '11279', '11284', '11292', '11295', '11320', '11348', '11351', '11354', '11408', '11436', '11439', '11440', '11445', '11447', '11469', '11473', '11501', '11512', '11561', '11788', '11865', '12056', '12112', '12179', '12256', '12339', '12370', '12724', '12741', '12765', '12809', '13058', '13104', '13137', '13331', '13398', '13445', '13593', '13613', '13759', '13796', '13822', '13936', '13983', '14062', '14088', '14202', '14246', '14333', '14468', '14483', '14577', '14605', '14608', '14701', '14711', '14712', '14715', '14731', '14736', '14773', '14798', '14825', '14843', '14852', '14857', '14862', '14874', '14920', '14928', '15011', '15027', '15035', '15070', '15075', '15101', '15131', '15152', '15203', '15219', '15221', '15237', '15249', '15273', '15275', '15310', '15331', '15342', '15356', '15358', '15373', '15404', '15427', '15431', '15439', '15441', '15445', '15479', '15482', '15528', '15529', '15530', '15559', '15561', '15577', '15582', '15594', '15606', '15607', '15611', '15617', '15623', '15657', '15660', '16173', '16225', '16247', '16264', '16343', '16355', '16375', '16380', '16416', '16430', '16502', '16531', '16542', '16571', '16581', '16601', '16729', '16774', '16830', '16849', '16863', '16869', '16910', '17004', '17035', '17036', '17085', '17110', '17321', '17324', '17503', '17585', '17619', '17625', '17682', '17690', '17726', '17741', '17987', '17992', '18001', '18020', '18073', '18084', '18098', '18122', '18216', '18217', '18256', '18327', '18353', '18358', '18429', '18626', '18653', '18700', '18990', '19002', '19064', '19156', '19186', '19192', '19208', '19217', '19258', '19263', '19543', '19727', '19823', '19833', '19843', '19880', '19944', '20196', '20228', '20315', '20347', '20352', '20395', '20426', '20449', '20463', '20464', '20506', '20818', '20858', '20941', '20990', '20995', '21050', '21052', '21250', '21276', '21288', '21292', '21345', '21512', '21528', '21562', '21612', '21696', '21713', '21728', '21776', '21795', '21850', '21867', '21915', '21920', '21947', '21954', '21958', '21983', '21996', '22018', '22037', '22077', '22126', '22127', '22147', '22171', '22179', '22184', '22190', '22205', '22207', '22244', '22254', '22281', '22306', '22338', '22360', '22370', '23656', '23665', '23718', '23729', '23872', '23879', '23915', '23916', '24137', '24391', '24644', '24787', '24792', '24979', '24985', '25111', '25153', '25199', '25322', '25410', '25415', '25421', '25432', '25442', '25449', '25510', '25529', '25539', '25545', '25588', '25602', '25637', '25650', '25688', '25693', '25733', '25774', '25848', '25877', '25892', '25907', '25976', '26001', '26110', '26116', '26120', '26122', '26135', '26138', '26147', '26179', '26194', '26212', '26222', '26242', '26256', '26332', '26337', '26484', '26539', '26619', '26761', '26869', '26964', '26992', '27101', '27137', '27145', '27157', '27218', '27220', '27319', '27352', '27356', '27447', '27522', '27621', '27626', '27629', '27722', '27733', '27762', '27782', '27795', '27825', '27925', '27996', '28025', '28066', '28072', '28129', '28168', '28213', '28348', '28361', '28392', '28414', '28612', '28632', '28651', '28692', '28703', '28719', '28835', '28864', '28871', '28986', '28989', '29030', '29064', '29125', '29138', '29221', '29300', '29323', '29328', '29447', '29477', '29496', '29522', '29574', '29594', '29650', '29668', '29715', '29762', '29857', '29947', '29958', '29969', '30018', '30276', '30285', '30583', '30611', '30703', '30706', '30771', '30959', '30960', '30964', '30987', '31039', '31041', '31061', '31135', '31261', '31296', '31337', '31602', '32146', '32271', '32314', '32320', '32332', '32412', '32429', '32461', '32483', '32518', '32548', '32553', '33312', '33323', '33391', '33489', '33505', '33602', '33764', '33769', '33866', '34007', '34129', '34130', '34132', '34184', '34337', '34356', '34368', '34369', '34390', '34421', '34428', '34448', '34479', '34544', '34600', '34636', '34639', '34654', '34665', '34753', '34826', '34831', '34866', '34899', '34954', '35010', '35028', '35045', '35067', '35080', '35083', '35086', '35113', '35118', '35153', '35221', '35256', '35306', '35308', '35365', '35384', '35458', '35480', '35490', '35544', '35551', '35664', '35773', '35787', '35837', '35868', '35871', '35882', '35884', '35955', '35957', '35993', '36038', '36064', '36098', '36166', '36228', '36239', '36240', '36329', '36464', '36492', '36555', '36559', '36631', '36642', '36659', '36744', '36816', '36817', '36818', '36831', '36969', '36971', '36976', '36990', '37015', '37040', '37161', '37222', '37323', '37333', '37338', '37348', '37511', '37719', '37724', '37759', '37761', '37825', '37827', '37870', '37933', '37965', '37970', '37986', '37998', '38009', '38014', '38101', '38158', '38260', '38265', '38326', '38479', '38497', '38553', '38563', '38585', '38596', '38609', '38645', '38653', '38738', '38771', '38792', '38838', '38858', '38963', '39016', '39031', '39047', '39064', '39102', '39112', '39215', '39231', '39261', '39287', '39345', '39378', '39512', '39574', '39589', '39650', '39679', '39684', '39708', '39712', '39723', '39743', '39807', '39831', '39833', '39908', '39968', '40021', '40066', '40097', '40099', '40144', '40157', '40179', '40191', '40238', '40257', '40272', '40305', '40309', '40348', '40362', '40410', '40425', '40449', '40459', '40479', '40535', '40543', '40572', '40587', '40651', '40658', '40673', '40722', '40725', '40740', '40792', '40799', '40820', '40868', '40876', '40884', '40901', '40903', '40923', '40946', '40961', '40973', '40999', '41007', '41009', '41015', '41021', '41052', '41081', '41085', '41101', '41114']

# ~ for partner_id in res_partner_ids:
    # ~ res_partner_domain = [('id', '=', int(partner_id))]
    # ~ migrate_model('res.partner', migrate_fields= res_partner_fields, include=True, domain = res_partner_domain)
# ~ res_partner_domain = [('id', '=', id) for id in res_partner_ids]
# ~ migrate_model('res.partner', migrate_fields= res_partner_fields, include=True, domain = res_partner_domain)
# ~ if debug:
    # ~ input("press enter to continue")

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # res.partner.bank fields to copy from source to target BROKEN
# ~ res_partner_bank_fields = ['acc_number', 'partner_id']
# ~ migrate_model('res.partner.bank', migrate_fields= res_partner_bank_fields, include=True, unique = ['acc_number'])

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # hr.employee fields to copy from source to target WORKS
# ~ hr_employee_fields = ['name', 'work_email', 'mobile_phone', 'work_location', 'company_id']
# ~ hr_employee_custom = {
    # ~ 'image_medium' : 'image_1920',
# ~ }
# ~ migrate_model('hr.employee', migrate_fields = hr_employee_fields, include=True, custom=hr_employee_custom)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # hr.department fields to copy from source to target WORKS
# ~ hr_department_fields = ['name']
# ~ migrate_model('hr.department', migrate_fields = hr_department_fields, include=True)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # hr.attendance fields to copy from source to target WORKS
# ~ hr_attendance_fields = ['name', 'work_email', 'mobile_phone', 'work_location', 'company_id']
# ~ hr_attendance_custom = {
    # ~ 'image_medium' : 'image_1920',
# ~ }
# migrate_model('hr.attendance', migrate_fields = hr_employee_fields, include=True, custom=hr_employee_custom)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # account.account.type fields to copy from source to target WORKING
# ~ account_type_field = ['name']
# ~ account_type_hard_code = {'type': 'receivable', 'internal_group': 'equity'}
# ~ migrate_model('account.account.type', migrate_fields = account_type_field, include=True, hard_code = account_type_hard_code)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # account.account fields to copy from source to target WORKING
# ~ account_fields = ['code', 'name', 'company_id']
# ~ account_custom = {'user_type': 'user_type_id'}
# ~ account_hard_code = {'reconcile': 1}
# ~ account_unique = ['code']
# ~ migrate_model('account.account', migrate_fields = account_fields, hard_code = account_hard_code, include=True, custom = account_custom, unique = account_unique)



# account.journal fields to copy from source to target WORKING
# ~ account_journal_fields = ['code', 'name', 'type']
# ~ account_journal_custom = {}
# ~ account_journal_hard_code = {'invoice_reference_model': 'odoo', 'invoice_reference_type': 'partner', 'company_id':1}
# ~ account_journal_unique = ['code']
# ~ migrate_model('account.journal', migrate_fields = account_journal_fields, hard_code = account_journal_hard_code, include=True, custom = account_journal_custom, unique = account_journal_unique)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ FIX PERIOD EXTERNAL ID 
# ~ source_to_target_dict = {
# ~ 200:1,    #opening
# ~ 201:2,    #01
# ~ 202:3,    #02
# ~ 203:4,    #03
# ~ 204:5,    #04
# ~ 205:6,    #05
# ~ 206:7,    #06
# ~ 207:8,    #07
# ~ 208:9,    #08
# ~ 209:10,    #09
# ~ 210:11,   #10
# ~ 211:12,    #11
# ~ 212:13,    #12
# ~ }

# ~ for source_id in source_to_target_dict:
    # ~ target_id = source_to_target_dict[source_id]
    # ~ create_xml_id('account.period',target_id,source_id)

# ~ # account.move fields to copy from source to target WORKING
# ~ account_move_fields = ['date', 'name', 'journal_id','period_id','state','tax_amount','credit','debit','balance','display_name','account_tax_id']
# ~ account_move_custom = {}
# ~ account_move_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
# ~ account_move_hard_code = {'move_type': 'entry'}
# ~ account_move_unique = ['name']
# ~ account_move_calc = {'currency_id': r" return source.env['account.move'].search_read(record['journal_id'], 'currency')"}
# ~ migrate_model('account.move', migrate_fields = account_move_fields, hard_code = account_move_hard_code, include=True, custom = account_move_custom, unique = account_move_unique,domain = account_move_domain)

# ~ account_move_line_fields = ['account_id', 'date', 'name', 'journal_id', 'move_id','credit','debit','display_name','account_tax_id','currency_id']
# ~ account_move_line_custom = {'account_tax_id':'tax_ids'}
# ~ account_move_line_domain = ['|',('period_id' ,'=',208),('date', '>=', '2021-08-01'),('date', '<=', '2021-08-31')]
# ~ account_move_hard_code = {'tax_id': 'tax_ids'}
# ~ account_move_unique = ['name']
# ~ account_move_line_calc = {'currency_id':r" return source.env['account.move.line'].search_read(record['journal_id'], 'currency')"}
# ~ migrate_model('account.move.line', migrate_fields = account_move_line_fields, include=True, custom = account_move_line_custom, unique = account_move_unique, domain = account_move_line_domain,calc = account_move_line_calc)



# ~ if debug:
    # ~ input("press enter to continue")

# ~ # account.invoice fields to copy from source to target BROKEN
# ~ account_invoice_fields = ['name', 'journal_id']
# ~ account_invoice_custom = {
    # ~ 'type': 'move_type',
    # ~ 'date_invoice': 'date'
    # ~ }
# ~ account_invoice_unique = ['name']
# ~ account_invoice_calc = {}
# ~ account_invoice_xml_id_suffix = 'b'
#migrate_model({'account.invoice': 'account.move'}, migrate_fields = account_invoice_fields, include=True, custom = account_invoice_custom, unique = account_invoice_unique, xml_id_suffix = account_invoice_xml_id_suffix)

# ~ if debug:
    # ~ input("press enter to continue")

# res.users fields to copy from source to target WORKS
# ~ res_users_fields = ['company_id', 'login', 'partner_id']
# ~ res_users_custom = {
    # ~ 'property_account_payable': 'property_account_payable_id',
    # ~ 'property_account_receivable': 'property_account_receivable_id'
# ~ }
# ~ res_users_hard_code = {
    # ~ 'notification_type': 'email'
# ~ }
# ~ res_users_ids = []
# ~ res_users_domain = [('id', '=', id) for id in res_users_ids]
# ~ res_users_unique = ['login']
# ~ migrate_model('res.users', migrate_fields = res_users_fields, include=True, custom=res_users_custom, hard_code=res_users_hard_code, unique=res_users_unique, domain = res_users_domain)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # product.pricelist fields to copy from source to target WORKING
# ~ product_pricelist_fields = ['name', 'code', 'display_name']
# ~ migrate_model('product.pricelist',migrate_fields = product_pricelist_fields, include=True, )

# ~ if debug:
    # ~ input("press enter to continue")

# product.pricelist.item fields to copy from source to target WORKING
# ~ product_pricelist_item_fields = ['price_discount', 'price_round', 'price_discount', 'price_min_margin', 'price_max_margin']
# ~ migrate_model('product.pricelist.item', migrate_fields = product_pricelist_item_fields , include=True, )

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # res.currency fields to copy from source to target WORKING i think?
# ~ res_currency_fields = ['name', 'symbol']
# ~ res_currency_unique = ['name']
# ~ migrate_model('res.currency', migrate_fields = res_currency_fields, include=True, unique = res_currency_unique)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # stock.location fields to copy from source to target WORKING
# ~ stock_location_fields = ['name', 'usage']
# ~ migrate_model('stock.location', migrate_fields = stock_location_fields, include=True, )

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # stock.warehouse fields to copy from source to target WORKING
# ~ stock_warehouse_fields = ['name', 'code', 'view_location_id', 'delivery_steps', 'reception_steps', 'partner_id', 'lot_stock_id', 'view_location_id']
# ~ stock_warehouse_unique = ['code']
# ~ migrate_model('stock.warehouse', migrate_fields = stock_warehouse_fields, include=True, unique = stock_warehouse_unique)

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # sale.order fields to copy from source to target WORKING
# ~ sale_order_fields = ['name', 'date_order', 'company_id', 'partner_id', 'partner_shipping_id', 'partner_invoice_id', 'picking_policy', 'pricelist_id', 'warehouse_id']
# ~ migrate_model('sale.order', migrate_fields = sale_order_fields, include=True, )

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # sale.order.line fields to copy from source to target WORKING
# ~ sale_order_line_fields = ['name', 'price_unit', 'product_uom_qty', 'order_id', 'company_id']
# ~ account_custom = {
    # ~ 'delay': 'customer_lead'
# ~ }
# ~ migrate_model('sale.order.line', migrate_fields = sale_order_line_fields, include=True, custom = account_custom, hard_code = {'product_id': 45})

# ~ if debug:
    # ~ input("press enter to continue")

# res.groups fields to copy from source to target NOT WORKING(cant migrate groups from 8, they work differently)
# ~ # res_groups_fields = ['name']
# ~ # res_groups_unique = ['name']
# ~ # migrate_model('res.groups', migrate_fields = res_groups_fields, include=True, unique = res_groups_unique, just_bind = True)

# ~ if debug:
    # ~ input("press enter to continue")

# product.public.category fields to copy from source to target WORKING
# ~ product_public_category_fields = ['name', 'display_name']
# ~ migrate_model('product.public.category', migrate_fields = product_public_category_fields, include=True, )

# ~ if debug:
    # ~ input("press enter to continue")

# ~ # product.attribute fields to copy from source to target WORKING
# ~ product_attribute_fields = ['name']
# ~ product_attribute_custom = {'type': 'display_type'} # create variant should be hardcoded to no_variant
# ~ product_attribute_hard_code = {'create_variant': 'always'}
# ~ migrate_model('product.attribute', migrate_fields = product_attribute_fields, include=True, custom = product_attribute_custom, hard_code = product_attribute_hard_code)

# ~ if debug:
    # ~ input("press enter to continue")


# ~ # product.attribute.value fields to copy from source to target WORKING
# ~ product_attribute_value_fields = ['name', 'attribute_id']
# ~ product_attribute_value_unique = ['name', 'attribute_id']
# ~ migrate_model('product.attribute.value', migrate_fields = product_attribute_value_fields, include=True, unique = product_attribute_value_unique)

# ~ if debug:
    # ~ input("press enter to continue")

# product.category fields to copy from source to target
# ~ product_category_fields = ['name']
# ~ product_category_custom = {
# ~ }
# ~ product_category_hard_code = {
    # ~ 'property_cost_method': 'standard',
    # ~ 'property_valuation': 'manual_periodic'
# ~ }
# ~ migrate_model('product.category', migrate_fields = product_category_fields, include=True, hard_code = product_category_hard_code)

# ~ if debug:
    # ~ input("press enter to continue")

# product.template fields to copy from source to target NEEDS uom.uom to be migrated, which is product.uom on odoo8
# ~ product_template_fields = ['name', 'active', 'sale_ok', 'purchase_ok', 'list_price', 'standard_price', 'description_sale', 'default_code', 'website_published', 'active', 'type', 'categ_id', 'sale_line_warn', ]
# ~ product_template_custom = {
    # ~ 'image_medium' : 'image_1920',
# ~ }
# ~ # Not used?
# ~ migrate_model('product.template', migrate_fields=product_template_fields, include=True, custom=product_template_custom, after_migration=product_tmpl_set_attributes, hard_code = {'company_id': 1})
# ~ #the old one had some weird checks for default code? incase it doesnt work

# ~ # product.product fields to copy from source to target
# ~ product_product_fields = ['name', 'active', 'sale_ok', 'description', 'purchase_ok', 'list_price', 'description_sale', 'default_code', 'active',
# ~ 'website_published', 'product_tmpl_id', 'lst_price', 'volume', 'standard_price', 'available_in_pos', 'weight',
# ~ 'ingredients', 'ingredients_last_changed', 'ingredients_changed_by_uid', 'use_desc', 'use_desc_last_changed', 'use_desc_changed_by_uid', 'event_ok']
# ~ product_product_custom = {
    # ~ 'image' : 'image_1920'
# ~ }
# ~ migrate_model('product.product', migrate_fields=product_product_fields, include=True, custom=product_product_custom)

# stock.move fields to copy from source to target WORKING
# ~ stock_move_fields = ['name', 'date', 'location_dest_id', 'location_id', 'procure_method', 'product_id', 'product_uom', 'product_uom_qty']
# ~ stock_move_hardcode = {
    # ~ 'company_id': 1
# ~ }
# ~ stock_move_domain = [('date', '>', '2020-09-1 10:10:10')]
# ~ migrate_model('stock.move', migrate_fields = stock_move_fields, include=True, hard_code = stock_move_hardcode, domain = stock_move_domain)

# ~ if default_variant_ids:
    # ~ target.env['product.product'].browse(default_variant_ids).unlink()
