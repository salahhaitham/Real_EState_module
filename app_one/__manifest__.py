{
    'name': 'Real Estate Management',
    'version': '1.0',
    'summary': 'My first custom module',
    'description': """
        هذا الموديول مثال لتعلم كيفية عمل Module في Odoo.
        يمكنك إضافة Models و Views هنا.
    """,
    'author': 'Salah',
    'category': 'Tools',
    'depends': ['base','sale','mail','account'],
    'assets': {
        'web.assets_backend': ['app_one/static/src/scss/property_form.css',],
        'web.report_assets_common': ['odoo/custom_addons/real_state_clean/app_one/static/src/scss/font.css'],


    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner2_view.xml',
        'views/tag_view.xml',
        'views/sales_view_form.xml',
        'reports/property_report.xml',
        'data/property_sequence.xml',
        'views/property_history_view.xml',
        'wizards/change_state.xml',
        'views/account_move.xml',





    ],
    'images': ['static/description/icon.png'],
    'demo': [

    ],

    'application': True,
'installable': True,
}
