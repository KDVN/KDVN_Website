# -*- coding: utf-8 -*-
{
    'name': "KDERP QA",

    'summary': """
        KINDEN VIETNAM Quality Control Website""",

    'description': """
        - Publish public information about QA for KDVN
        - At internal control: manage document related to QA
    """,

    'author': "KINDEN VIETNAM",
    'website': "http://www.kinden.co.jp",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}