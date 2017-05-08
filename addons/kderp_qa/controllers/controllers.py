# -*- coding: utf-8 -*-
from openerp import http

# class KderpQa(http.Controller):
#     @http.route('/kderp_qa/kderp_qa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kderp_qa/kderp_qa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kderp_qa.listing', {
#             'root': '/kderp_qa/kderp_qa',
#             'objects': http.request.env['kderp_qa.kderp_qa'].search([]),
#         })

#     @http.route('/kderp_qa/kderp_qa/objects/<model("kderp_qa.kderp_qa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kderp_qa.object', {
#             'object': obj
#         })