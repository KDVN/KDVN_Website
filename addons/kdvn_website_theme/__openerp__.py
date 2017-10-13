# -*- coding: utf-8 -*-
{
    'name': "KDVN Website Theme",
    'summary': """KINDEN VIETNAM Website theme""",
    'description': """
                   KINDEN VIETNAM Website theme
                """,
    'author': "KDVN IT Team",
    'website': "http://www.kinden.jp.co",
    'category': "Kdvn",
    'version': "0.1",
    'depends': ['kdvn_website'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
			'data/menu_data.xml',
			'data/data.xml',
			'data/content_data.xml',
			'views/config_view.xml',
			'views/assets_temp.xml',				
			'views/header_footer_temp.xml',
			'views/recruitment_temp.xml',
			'views/snippets_temp.xml',			
            'views/templates.xml',	
						
            ]
}