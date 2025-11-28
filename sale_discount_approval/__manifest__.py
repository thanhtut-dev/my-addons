# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Discount Approval',
    'version': '16.0',
    'category': 'Sales',
    'description': 'Sales order discount approval workflow with multi-level rules.',
    'depends': ['base', 'web', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_discount_approval_security.xml',
        'data/mail_templates.xml',
        'views/sale_order_views.xml',
        'views/approval_menus.xml',
        ],
    'installable': True,
}
