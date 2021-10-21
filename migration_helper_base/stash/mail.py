# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    last_migration_date = fields.Datetime()
