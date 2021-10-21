#!/usr/bin/env python3

from configuration import *

depends = {
    'base': {'dependencies': [], },

    'social_media': {'dependencies': ['base'], },
    'uom': {'dependencies': ['base'], },
    'web': {'dependencies': ['base'], },

    'base_setup': {'dependencies': ['base', 'web'], },
    'barcodes': {'dependencies': ['web'], },
    'bus': {'dependencies': ['base', 'web'], },
    'http_routing': {'dependencies': ['web'], },
    'resource': {'dependencies': ['base', 'web'], },
    'utm': {'dependencies': ['base', 'web'], },
    'web_editor': {'dependencies': ['web'], },
    'web_tour': {'dependencies': ['base'], },

    'google_recaptcha': {'dependencies': ['base_setup'], },
    'mail': {'dependencies': ['base', 'base_setup', 'bus', 'web_tour'], },

    'auth_signup': {'dependencies': ['base_setup', 'mail', 'web'], },
    'analytic': {'dependencies': ['base', 'mail', 'uom'], },
    'hr': {'dependencies': ['base_setup', 'mail', 'resource', 'web'], },
    'product': {'dependencies': ['base', 'mail', 'uom'], },
    'rating': {'dependencies': ['mail'], },
    'sales_team': {'dependencies': ['base', 'mail'], },

    'hr_contract': {'dependencies': ['hr'], },
    'hr_timesheet': {'dependencies': ['analytic', 'hr', 'project', 'uom'], },
    'portal': {'dependencies': ['auth_signup', 'http_routing', 'mail', 'web', 'web_editor'], },

    'digest': {'dependencies': ['mail', 'portal', 'resource'], },
    'portal_rating': {'dependencies': ['portal', 'rating'], },

    'account': {'dependencies': ['analytic', 'base_setup', 'digest', 'portal', 'product'], },
    'project': {'dependencies': ['analytic', 'base_setup', 'digest', 'mail', 'portal', 'rating', 'resource', 'web', 'web_tour'], },
    'stock': {'dependencies': ['barcodes', 'digest', 'product'], },
    'website': {'dependencies': ['auth_signup', 'digest', 'http_routing', 'portal', 'social_media', 'web', 'web_editor'], },

    'hr_expense': {'dependencies': ['account', 'hr_contract', 'web_tour'], },
    'mrp': {'dependencies': ['product', 'resource', 'stock'], },
    'product_expiry': {'dependencies': ['stock'],
                       'fields': ['alert_time', 'expiration_time', 'removal_time', 'use_expiration_date', 'use_time'], },
    'purchase': {'dependencies': ['account'], },
    'payment': {'dependencies': ['account'], },
    'stock_account': {'dependencies': ['account', 'stock'], },
    'website_form': {'dependencies': ['google_recaptcha', 'mail', 'website'], },
    'website_mail': {'dependencies': ['mail', 'website'], },

    'mrp_account': {'dependencies': ['mrp', 'stock_account'], },
    'purchase_stock': {'dependencies': ['purchase', 'stock_account'], },
    'sale': {'dependencies': ['payment', 'portal', 'sales_team', 'utm'], },
    'website_payment': {'dependencies': ['payment', 'portal', 'website'], },

    'sale_management': {'dependencies': ['digest', 'sale'], },
    'sale_product_configurator': {'dependencies': ['sale'], },
    'sale_stock': {'dependencies': ['sale', 'stock_account'], },
    'stock_landed_cost': {'dependencies': ['stock_account', 'purchase_stock'], },
    'website_sale': {'dependencies': ['digest', 'portal_rating', 'sale', 'website', 'website_form', 'website_mail', 'website_payment'], },

    'sale_project': {'dependencies': ['project', 'sale_management'], },
    'website_sale_product_configurator': {'dependencies': ['sale_product_configurator', 'website_sale'], },
    'website_sale_stock': {'dependencies': ['sale_stock', 'website_sale'], },
    'mrp_landed_costs': {'dependencies': ['mrp', 'stock_landed_cost'], },

    'sale_timesheet': {'dependencies': ['hr_timesheet', 'sale_project'],
                       'fields': ['project_id', 'project_template_id', 'service_policy', 'service_type']},
    'purchase_requisition': {'dependencies': ['purchase'],
                             'fields': ['purchase_requisition']},
}
all_module = source.env['ir.module.module'].search_read(
    [], ['name', 'dependencies_id'], order='name')
all_module_dependency = source.env['ir.module.module.dependency'].search_read(
    [], ['name'])
all_module2 = {x['name']: {'dependency': sorted(next(
    z['name'] for z in all_module_dependency if z['id'] == y) for y in x['dependencies_id'])} for x in all_module}


def count_modules(module, modules=set()):
    modules.add(module)
    dependencies = depends[module].get('dependency')
    if dependencies:
        for m in dependencies:
            modules.union(count_modules(m, modules))
    return modules


module = input('module: ')

print(sorted(count_modules(module)))
print(len(count_modules(module)))


