# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    last_migration_date = fields.Datetime()


class ProductAttributeCustomValue(models.Model):
    _inherit = "product.attribute.custom.value"
    
    last_migration_date = fields.Datetime()
    
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    last_migration_date = fields.Datetime()


class ProductCategory(models.Model):
    _inherit = "product.category"

    last_migration_date = fields.Datetime()


class ProductPackaging(models.Model):
    _inherit = "product.packaging"
    
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


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    last_migration_date = fields.Datetime()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_migration_date = fields.Datetime()


class ProductTemplateAttributeExclusion(models.Model):
    _inherit = "product.template.attribute.exclusion"
    
    last_migration_date = fields.Datetime()
    
    
class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    last_migration_date = fields.Datetime()

    
class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    last_migration_date = fields.Datetime()


