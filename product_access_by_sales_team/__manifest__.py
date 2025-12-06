# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Access by Sales Team',
    'version': '18.0',
    'category': 'Sales',
    'summary': '',
    'description': 'static/description/index.html',
    'images': ['static/description/thumbnail.png'],
    'author': 'thanhtut-dev',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['account','crm','sale','sales_team','sale_management','web'],
    'data': [
            'views/crm_team_views.xml',
            'views/sale_order_views.xml',
            'views/sale_order_template_view.xml',
        ],
    'installable': True,
    'application': True,
}
