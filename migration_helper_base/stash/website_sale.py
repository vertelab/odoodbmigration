# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    last_migration_date = fields.Datetime()
