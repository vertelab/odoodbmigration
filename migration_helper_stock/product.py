# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    last_migration_date = fields.Datetime()


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    last_migration_date = fields.Datetime()


class ProductCategory(models.Model):
    _inherit = "product.category"

    last_migration_date = fields.Datetime()


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    last_migration_date = fields.Datetime()


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    last_migration_date = fields.Datetime()


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_migration_date = fields.Datetime()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_migration_date = fields.Datetime()
