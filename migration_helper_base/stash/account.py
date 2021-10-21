# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    last_migration_date = fields.Datetime()


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    last_migration_date = fields.Datetime()


class AccountJournal(models.Model):
    _inherit = "account.journal"

    last_migration_date = fields.Datetime()


class AccountMove(models.Model):
    _inherit = "account.move"

    last_migration_date = fields.Datetime()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    last_migration_date = fields.Datetime()
