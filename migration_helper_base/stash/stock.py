# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    last_migration_date = fields.Datetime()


class StockMove(models.Model):
    _inherit = "stock.move"

    last_migration_date = fields.Datetime()


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    last_migration_date = fields.Datetime()
