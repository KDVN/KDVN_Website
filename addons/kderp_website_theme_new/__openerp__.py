{
    #Theme infomation
    'name':'Kderp Website Theme New',
    'description':"""
		Kderp Website Theme New Theo style Kinden Thai lan.
		Ke thua co module sau:
			- Kderp Website Theme Default Thuy2
			- Kderp Website Theme Default Thuy1
			- Kderp Website Theme Default
			- Kderp Website
		De hien thi lai cac theme cu can upgrade lai cac mudule tren:
			- Kderp Website Theme Default Thuy2
			- Kderp Website Theme Default Thuy1
			- Kderp Website Theme Default
		Them cac bieu tuong vao menu header
			1. Go to the Font-Awesome website, select your icon (e.g.: 'fa-eye')
			2. Go to Settings > Configuration > Website Settings > Menu > Configure website menus > Font Awesome Icon
			3. Select the menu you want to add / change the icon
			4. Paste the fa code (e.g.: 'fa-eye') in Font Awesome Icon
		Cac bieu tuong trong menu header
			- fa fa-home
			- fa fa-info-circle
			- fa-building-o
			- fa fa-globe
			- fa fa-calendar
			- fa fa-user
		Cac position tuong ung voi cac dia diem
			- Noi Bai Office: 21.2327297,105.8106964
			- Thang Long Office: 21.1155719,105.7758676
			- Hung Yen Office: 20.9399806,106.0413451
			- Binh Duong Office: 10.94354079054853,106.73663017381898
			- Bien Hoa Office: 10.9283772,106.875574	
			- HO: 21.0304207,105.784361
    """,
    'category':'test',
    'version':'1.0',
    'depends':['kderp_website_theme_default_thuy2'],
    
    #tempalte, pages, and snippets
    'data':[
            # 'security/security.xml',
			# 'security/ir.model.access.csv',
            'views/layout.xml',
            'views/pages.xml',
            'views/data.xml',
            'views/assets.xml',
            'views/snippets.xml',
			'views/kderp_website_views.xml',
            ],
    
    #Information
    'author': "IT_Kinden",
    'website':"www.kinden.com.vn",
    'application':True,
}