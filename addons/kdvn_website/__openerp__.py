# -*- coding: utf-8 -*-
{
    'name': "KDVN Website",
    'summary': """KINDEN VIETNAM Website""",
    'description': """
					KINDEN VIETNAM Website backend					
                """,
    'author': "KDVN IT Team",
    'website': "http://www.kinden.jp.co",
    'category': "Kdvn",
    'version': "0.1",
    'depends': ['website_blog','website_hr_recruitment','website_crm'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
			'data/data_menu.xml',
			'data/data.xml',
			'views/templates.xml',
			'views/res_flag_views.xml',		
            'views/blog_views.xml',
			'views/res_partner_views.xml',
			'views/action_menu_views.xml',
			'views/hr_views.xml',
            'views/templates.xml',	
            ]
}