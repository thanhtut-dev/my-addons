# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Action Access',
    'version': '18.0',
    'category': 'Sales',
    'summary': 'Restrict POS actions using employee-level permissions.',
    'description': 'static/description/index.html',
    'images': ['static/description/thumbnail.png'],
    'author': 'thanhtut-dev',
    'website': 'https://thanhtut-dev.odoo.com/',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'hr', 'pos_hr'],
    'data': [
        'views/hr_employee_views.xml',
        ],
    'assets': {
            'point_of_sale._assets_pos': [
                'pos_control_buttons_access/static/src/app/screens/product_screen/product_screen.js',
                'pos_control_buttons_access/static/src/app/screens/product_screen/control_buttons/control_buttons.xml',
                'pos_control_buttons_access/static/src/app/screens/ticket_screen/ticket_screen.xml',
                'pos_control_buttons_access/static/src/app/screens/product_screen/action_pad.js',
                'pos_control_buttons_access/static/src/app/screens/product_screen/action_pad.xml',

            ],
        },
    'installable': True,
    'application': True,
}
