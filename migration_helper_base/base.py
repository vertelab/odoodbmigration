# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    last_migration_date = fields.Datetime()


class IrModelData(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def find_all_ids_in_target(self, model, module=False):
        if not module:
            module = self.env['ir.config_parameter'].sudo().get_param(
                'migration_helper.import_module_string', default='__import__')

        query = (
            f"SELECT NULLIF(regexp_replace(name, '\D','','g'), '')::int4 AS result FROM ir_model_data WHERE module = '{module}' AND model = '{model}'"
        )
        self.env.cr.execute(query)
        return [int(r["result"]) for r in self.env.cr.dictfetchall()]


class Partner(models.Model):
    _inherit = "res.partner"

    last_migration_date = fields.Datetime()


class ResCurrency(models.Model):
    _inherit = "res.currency"

    last_migration_date = fields.Datetime()


class ResGroups(models.Model):
    _inherit = "res.groups"

    last_migration_date = fields.Datetime()


class ResUsers(models.Model):
    _inherit = "res.users"

    last_migration_date = fields.Datetime()
