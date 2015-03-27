# -*- coding: utf-8 -*-
from openerp import http

class Openacademy(http.Controller):
    @http.route('/openacademy/', auth='public', website=True)
    def index(self):
        Courses = http.request.env['openacademy.course']
        
        return http.request.render('openacademy.index', {
            'courses': Courses.search([]),
            })
        
    @http.route('/openacademy/<int:id>', auth='public', website=True)
    def course(self, id):
        return '<h1>{} ({})</h1>'.format(id, type(id).__name__)
    
    @http.route('/openacademy/<model("openacademy.courses"):responsible>', auth='public', website=True)
    def responsible(self, responsible):
        return http.request.render('openacademy.responsible', {
                'person': responsible
            })
# class Openacademy(http.Controller):
#     @http.route('/openacademy/openacademy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openacademy/openacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy.listing', {
#             'root': '/openacademy/openacademy',
#             'objects': http.request.env['openacademy.openacademy'].search([]),
#         })

#     @http.route('/openacademy/openacademy/objects/<model("openacademy.openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy.object', {
#             'object': obj
#         })