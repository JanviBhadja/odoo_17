{
    'name': 'Online Shopping',
    'version': '1.1',
    'author': 'Janvi Bhadja',
    'summary': 'E Commerce Online shopping system',
    'description': '',
    'sequence': 10,
    'category': 'E Commerce',
    'depends': ['base', 'hr_expense', 'web', 'stock', 'sale', 'sale_management', 'sale_stock'],

    'assets': {
        'web.assets_backend': [
            "Online_shopping/static/src/views/js/inherited_view.xml",
            "Online_shopping/static/src/views/js/inherited_button.js"
        ],
    },

    'data': [
        "security/ir.model.access.csv",
        "security/shopping_groups.xml",
        "wizard/cancel_order_wizard_view.xml",
        "wizard/sale_report_wizard_view.xml",
        "wizard/excel_report_wizard_view.xml",
        "report/report_actions.xml",
        "report/order_report_templates.xml",
        "report/sale_order_report.xml",
        "report/sale_order_report_templates.xml",
        "report/order_delivery_report.xml",
        "report/commission_report.xml",
        "report/res_partner_email_template_report.xml",
        "data/res_partner_template.xml",
        "data/bday_reminder_cron.xml",
        "views/menu_view.xml",
        "views/product_view.xml",
        "views/category_view.xml",
        "views/customer_view.xml",
        "views/order_view.xml",
        "views/order_item_view.xml",
        "views/product_delivery_view.xml",
        "views/commission_view.xml",
        "views/commission_on_line_view.xml",
        "views/inherited_fields_view.xml"
    ],  
    'installable': True,
    'application': True,
    'auto_install': False
}
