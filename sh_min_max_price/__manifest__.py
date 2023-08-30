# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

{
    'name': 'Minimum And Maximum Price Of Product',
    'author': 'Softhealer Technologies',
    "license": "OPL-1",
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'version': '15.0.3',
    'category': 'Sales',
    'summary': """product pricelist management product minimum price product maximum price min product price Max product price Minimum Price Of Product Purchase Price maximum selling price minimum selling price On Product odoo""",
    'description': """This module useful to set minimum and maximum selling price for product. Sales person can easily see minimum and maximum sale price so that will useful to make clear action in sales procedure without waiting for senior person.
    product pricelist module, pricelist management app, set product minimum price, select product maximum price, min –max product price odoo
    """,
    'depends': ['sale_management', 'sh_base_min_max_price'],
    'data': [
        'data/sale_order_price_group.xml',
        'views/sale_order_min_max_price.xml',
    ],
    'images': ['static/description/background.png', ],
    'auto_install': False,
    'installable': True,
    'application': True,
    "price": 15,
    "currency": "EUR"
}
