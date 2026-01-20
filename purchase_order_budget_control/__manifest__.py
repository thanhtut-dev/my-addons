# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Department Purchase Budget Control',
    'version': '17.0',
    'category': 'Inventory/Purchase',
    'summary': 'Department-based Purchase Budget Control with Automatic Approval Workflow.',
    'description': 'static/description/index.html',
    'images': ['static/description/thumbnail.png'],
    'author': 'thanhtut-dev',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['base','purchase'],
    'data': [
        'security/data.xml',
        'security/ir.model.access.csv',
        'views/purchase_budget_view.xml',
        'views/purchase_order_view.xml',
        ],
    'installable': True,
    'application': True,
}
