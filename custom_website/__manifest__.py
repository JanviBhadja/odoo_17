{
    'name': 'Custom Website',
    'version': '17.0.0.1',
    'authors': 'Jani Bhadja',
    'summary': 'Custom Website',
    'description': 'Custom Website',
    'sequence': -1,
    'category': 'website',
    'depends': ['base','website','sale'],
    'assets': {
        'web.assets_frontend':[
            "custom_website/static/src/js/submit_button.js",
        ],
    },

    'data': [
        'views/website_menu.xml',
        'views/view_template.xml',
    ],

}