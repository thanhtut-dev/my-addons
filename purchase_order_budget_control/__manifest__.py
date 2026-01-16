# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Order Budget Control By Department',
    'version': '17.0',
    'category': 'Inventory/Purchase',
    'summary': 'Control purchase orders using department-based budget limits.',
    'author': 'thanhtut-dev',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_budget_view.xml',
        'views/purchase_order_view.xml',
        ],
    'installable': True,
    'application': True,
}
