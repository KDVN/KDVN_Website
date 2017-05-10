{
    #Theme infomation
    'name':'Kderp Website Theme Default Thuy2',
    'description':"""
        Kderp Website Theme Default Thuy2
    """,
    'category':'test',
    'version':'1.0',
    'depends':['kderp_website', 'kderp_website_theme_default', 'website_menu_by_user_status', 'kderp_event', 'website_hr_recruitment'],
    
    #tempalte, pages, and snippets
    'data':[
            'security/security.xml',
			'security/ir.model.access.csv',
            'views/layout.xml',
            'views/pages.xml',
            'views/data.xml',
            'views/assets.xml',
            'views/res_flag.xml',
            'views/contact_us.xml',
            'views/snippets.xml',
            'views/hr.xml',
            'views/views.xml',
            ],
    
    #Information
    'author': "IT_Kinden",
    'website':"www.kinden.com.vn",
    'application':True,
}