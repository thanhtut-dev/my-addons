# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Quotation Discount Approval',
    'version': '16.0.1',
    'category': 'Sales',
    'summary': 'Approval workflow for Sales quotation discounts with email notifications',
    'description': 'static/description/index.html',
    'images': ['static/description/mail_approve.png'],
    'author': 'Than Htut',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': [ 'sale','sales_team', 'mail'],
    'data': [
        'security/sale_discount_approval_security.xml',
        'data/mail_templates.xml',
        'views/sale_order_views.xml',
        'views/crm_team_views.xml',
        'views/approval_menus.xml',
        ],
    'installable': True,
    'application': True,
}
