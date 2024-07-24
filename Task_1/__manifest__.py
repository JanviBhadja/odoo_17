{
    'name': 'Volume Discount',
    'version': '17.0.0.1',
    'authors': 'Jani Bhadja',
    'summary': 'Apply total discount on Sale Order Line',
    'description': 'Apply discount on sales order line',
    'sequence': 10,
    'depends': ['base','sale','product'],
    'data': [
        'security/ir.model.access.csv',

        'views/menu.xml',
        'views/volume_discount.xml',
        'views/sale_order_line.xml',
        'views/discount_history_tracking.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}