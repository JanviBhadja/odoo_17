# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: Cybersource',
    'version': '2.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "An Irish-American payment provider covering the US and many others.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['base', 'sale', 'payment'],
    'data': [
        'views/payment_provider.xml',
        # 'views/payment_stripe_templates.xml',
        # 'views/payment_templates.xml',  # Only load the SDK on pages with a payment form.

        'data/payment_provider_data.xml',  # Depends on views/payment_stripe_templates.xml
    ],
    'license': 'LGPL-3',
}
