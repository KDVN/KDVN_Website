# -*- coding: utf-8 -*-
from openerp import http

# class KderpWebsite(http.Controller):
#     @http.route('/kderp_website/kderp_website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kderp_website/kderp_website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kderp_website.listing', {
#             'root': '/kderp_website/kderp_website',
#             'objects': http.request.env['kderp_website.kderp_website'].search([]),
#         })

#     @http.route('/kderp_website/kderp_website/objects/<model("kderp_website.kderp_website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kderp_website.object', {
#             'object': obj
#         })

class KderpWebsite(http.Controller):
    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('kderp_website.index',{
            'teachers': ["Thanh", "Duong", "Kajiya"],
        })
    
    @http.route('/kderp_website/contacts', auth='public', website=True)
    def contacts(self, **kw):
        """Showing all contacts name"""
        Contacts = http.request.env['res.partner']
        return http.request.render('kderp_website.contacts',{
            'contacts': Contacts.search([('category_id.name','=','KDVN_Office')])
        })
        
    def offices(self):
        return http.request.env['res.partner'].search([('category_id.name','=','KDVN_Office')])
        
