# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Customer Access by Sales Team',
    'version': '17.0.1',
    'category': 'Sales',
    'summary': 'Restrict salespersons to customers assigned to their Sales Team, and allow access only to Sale Orders,'
            'CRM Leads, and Opportunities created by their own team.',
    'description': 'static/description/index.html',
    'images': ['static/description/thumbnail.png'],
    'author': 'thanhtut-dev',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['account','crm','sale','sales_team','web'],
    'data': [
            'views/crm_team_views.xml',
            'views/sale_order_views.xml',
            'views/crm_lead_views.xml',
        ],
    'installable': True,
    'application': True,
}
