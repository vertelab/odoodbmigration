# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProjectScrumPortfolio(models.Model):
    _inherit = "project.scrum.portfolio"

    last_migration_date = fields.Datetime()


class ProjectScrumTimebox(models.Model):
    _inherit = "project.scrum.timebox"

    last_migration_date = fields.Datetime()
