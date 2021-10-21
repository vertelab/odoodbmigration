# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProjectScrumActors(models.Model):
    _inherit = "project.scrum.actors"

    last_migration_date = fields.Datetime()


class ProjectScrumSprint(models.Model):
    _inherit = "project.scrum.sprint"

    last_migration_date = fields.Datetime()


class ProjectScrumTest(models.Model):
    _inherit = "project.scrum.test"

    last_migration_date = fields.Datetime()


class ProjectScrumUS(models.Model):
    _inherit = "project.scrum.us"

    last_migration_date = fields.Datetime()
