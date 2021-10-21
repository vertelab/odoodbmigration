# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"

    last_migration_date = fields.Datetime()


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    last_migration_date = fields.Datetime()
