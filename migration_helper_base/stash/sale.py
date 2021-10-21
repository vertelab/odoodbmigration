# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    last_migration_date = fields.Datetime()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    last_migration_date = fields.Datetime()
