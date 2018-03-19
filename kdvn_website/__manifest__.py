# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'KDVN Website',
    'version': '1.0',
    'category': 'Kdvn',
    'description': "KINDEN VIETNAM Website backend	",
    'website': 'http://www.kinden.jp.co',
    'summary': 'KINDEN VIETNAM Website',
    'sequence': 45,
    'depends': [
        'document','website_blog','website_crm'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
		'data/menu_data.xml',
		'data/data.xml',
		'data/content_data.xml',
		'views/res_partner_views.xml',
		'views/blog_views.xml',
		'views/action_menu_views.xml',
		'views/templates.xml',
    ],
    'demo': [
        
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
