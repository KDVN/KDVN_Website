# -*- coding: utf-8 -*-
{
    'name': "KDVN Website",
    'summary': """KINDEN VIETNAM Web site""",
    'description': """
                    Providing means for customize KDVN Website
                    - Maximizing feeding information automatically
                    - Adding configurations for the website
                    - Providing basic theme
                    Providing General information, News, QA section
                    And a kind of portal to employees
                    """,
    'author': "KDVN IT Team",
    'website': "http://www.kinden.jp.co",
    'category': "Test",
    'version': "0.1",
    'depends': ['web', 'website', 'website_partner', 'website_blog'],
    'data': [
             'security/security.xml',
             'security/ir.model.access.csv',
             'data/data.xml',
             'views/inherited_kderp_website_views.xml',
             'views/kderp_website_about.xml',
             'views/kderp_website_event.xml',
             'views/kderp_website_footer.xml',
             'views/kderp_website_header.xml',
             'views/kderp_website_homepage.xml',
             'views/kderp_website_templates.xml',
             'views/kderp_website_views.xml'
             ]
}