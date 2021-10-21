# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    last_migration_date = fields.Datetime()


class ProjectTags(models.Model):
    _inherit = "project.tags"

    last_migration_date = fields.Datetime()


class ProjectTask(models.Model):
    _inherit = "project.task"

    last_migration_date = fields.Datetime()


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    last_migration_date = fields.Datetime()
