# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'KDVN Website Structure',
    'category': 'Kdvn',
    'website': 'http://www.kindenvietnam.com.vn',
    'summary': 'KINDEN VIETNAM Website Structure',
    'version': '1.0',
    'description': "",
    'depends': ['kdvn_website'],
    'data': [
		'security/security.xml',
		'security/ir.model.access.csv',		
		'data/menu_data.xml',		
		'views/config_view.xml',
		'views/header_footer_temp.xml',
		'views/templates.xml',		
    ],
    'demo': [
    ],
    'test': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
