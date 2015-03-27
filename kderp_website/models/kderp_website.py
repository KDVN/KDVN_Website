import openerp
from openerp import http
from openerp.osv import orm, osv
from openerp import models, fields, api

from openerp import SUPERUSER_ID

#def offices():
#    return http.request.env['res.partner'].search([('category_id.name','=','KDVN_Office')])

"""
class res_partner(osv.osv):
    _inherit = "res.partner"
    def offices(self):
        return self.pool.get('res.partner')
   
"""
 
"""
class view(osv.osv):
    _inherit = "ir.ui.view"
    
    @api.cr_uid_ids_context
    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb', context=None):
        
        
        rp_ids = self.pool['res.partner'].search(cr, uid,[('category_id.name','=','KDVN_Office')])
        offices = self.pool['res.partner'].browse(cr, uid, rp_ids)
        offices = self.pool['res.users'].browse(cr, uid, uid).company_id.partner_id.child_ids
        kdvn_offices = {"kdvn_offices":offices}
        if not values:
            values = dict()
        values.update(kdvn_offices)
        return super(view, self).render(cr, uid, id_or_xml_id, values=values, engine=engine, context=context)
""" 

class KdvnNewsTags(models.Model):
    _name = 'kdvn.news.tags'
    
    name = fields.Char(string="Tags")
    

class KdvnNews(models.Model):
    _inherit = 'blog.blog'

    blogpost_ids = fields.One2many('blog.post', 'blog_id', string="Blog Posts")
    
class KdvnOffice(models.Model):
    _inherit = 'res.partner'
    

