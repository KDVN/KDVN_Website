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
    'depends': ['website', 'website_partner', 'website_blog'],
    'data': [
             'data/data.xml',
             'views/website_templates.xml',
             'views/views.xml',
             'views/pages.xml',
             ],
    'demo': [
             'demo.xml',
             ],
}