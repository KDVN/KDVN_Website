{
    'name': 'KDVN Theme',
    'category': 'Test',
    'version': '1.0',
    'description':
        """
Theme for odoo
========================

This module for theme testing
        """,
    'depends': ['website', 'kderp_website'],
    'data': [
             'views/pages.xml', 'views/snippets.xml',
             ],
    'application': True,
}
