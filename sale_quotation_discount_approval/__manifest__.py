# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sale Discount Approval',
    'version': '16.0.1',
    'category': 'Sales',
    'description': 'Sales order discount approval workflow with Brevo SMTP Server. '
                   'Allows manager/supervisor approval based on discount thresholds.',
    'author': 'Than Htut',
    'website': 'https://github.com/thanhtut-dev',
    'license': 'OPL-1',
    'depends': ['base', 'web', 'sale','sales_team', 'mail'],
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
