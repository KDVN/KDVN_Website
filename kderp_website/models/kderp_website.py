import openerp
from openerp import http
from openerp.osv import orm, osv
from openerp import models, fields, api

from openerp import SUPERUSER_ID


class view(osv.osv):
    """Modify render method to add KDVN information to the homepage"""
    _inherit = "ir.ui.view"
    
    @api.cr_uid_ids_context
    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb', context=None):
        
        rp_ids = self.pool['res.partner'].search(cr, uid,[('category_id.name','=','KDVN_Office')])
        offices = self.pool['res.partner'].browse(cr, uid, rp_ids)
        offices = self.pool['res.users'].browse(cr, uid, uid).company_id.partner_id.child_ids
        kdvn_offices = {"kdvn_offices":offices}
        
        tag_list = ['KinQ News','KinVQ News']
        news_list = ['General News', 'IT', 'Quality Safety Assurance', 'Electrical Systems', 'Mechanical Systems']
        #KDVN hot news
        #TODO: offset and limit need to be variables
        #
         
        # sudung map va reduce de lay join recordset cua post tra ve tu blog.tag
        tags = http.request.env['blog.tag'].search([('name', 'in', tag_list)])
        post_ids = tags.mapped('post_ids').mapped('id')
        
        news_ids = self.pool['blog.post'].search(cr, uid, [('blog_id', 'in', news_list), ('id', 'not in', post_ids)], offset=0, limit=8)
        news = self.pool['blog.post'].browse(cr, uid, news_ids)
        #kdvn_news_e
        news_e_ids = self.pool['blog.post'].search(cr, uid, [('blog_id', '=', 'Electrical Systems')], offset=0, limit=2)
        news_e = self.pool['blog.post'].browse(cr, uid, news_e_ids)
        #kdvn_news_m
        news_m_ids = self.pool['blog.post'].search(cr, uid, [('blog_id', '=', 'Mechanical Systems')], offset=0, limit=2)
        news_m = self.pool['blog.post'].browse(cr, uid, news_m_ids)
        #kdvn_news_q
        news_q_ids = self.pool['blog.post'].search(cr, uid, [('blog_id', '=', 'Quality Safety Assurance')], offset=0, limit=2)
        news_q = self.pool['blog.post'].browse(cr, uid, news_q_ids)
        #KDVN works
        work_tag = "KDVN_Works"
        works_ids = self.pool['blog.post'].search(cr, uid, [('tag_ids','=', work_tag)], offset=0)
        works = self.pool['blog.post'].browse(cr, uid, works_ids)
        
        #KDVN ME
        me_ids = self.pool['blog.post'].search(cr, uid, [('blog_id','=','Introduction'),('name', 'in', ['Mechanical Systems', 'Electrical Systems', 'QST'])], order="name")
        me = self.pool['blog.post'].browse(cr, uid, me_ids)
        
        kdvn_info = {"kdvn_news":news, "kdvn_works":works, "kdvn_me": me, "kdvn_news_e":news_e, "kdvn_news_m":news_m, "kdvn_news_q":news_q}

        if not values:
            values = dict()
        values.update(kdvn_info)
        return super(view, self).render(cr, uid, id_or_xml_id, values=values, engine=engine, context=context)
 
class website_menu(osv.osv):
    """
    - Adding divider option to menu
    - TODO: How to use both old and new api correctly, ex: fields
    """
    _inherit = "website.menu"
    _columns = {
        'divider': openerp.osv.fields.boolean('Divider', default=False),
        'divider_text': openerp.osv.fields.char('Divider Text', translate=True)
    }
    

class KdvnNewsTags(models.Model):
    _name = 'kdvn.news.tags'
    
    name = fields.Char(string="Tags")
    

class KdvnNews(models.Model):
    _inherit = 'blog.blog'
    
    blogpost_ids = fields.One2many('blog.post', 'blog_id', string="Blog Posts")
    
class KdvnPost(models.Model):
    _inherit = 'blog.post'
    
    @api.one
    def _get_img_url_ids(self):
        result = []
        attachments = self.env['ir.attachment'].search([('res_model','=','blog.post'),('res_id','=',self.id)])
        
        for att in attachments:
            result.append(att.id)
        
#         import pdb
#         pdb.set_trace()
        self.img_url_ids = result


    img_url_ids = fields.One2many('ir.attachment', string="Image URLs", compute='_get_img_url_ids')
    #img_url_ids = fields.One2many('ir.attachment', 'id')
    summary = fields.Text('Summary', translate=True)    

class event(osv.osv):
    """Modify some methods of event object:
    - Change Google map zoom default to 12
    
    TODO: not yet
    """
    _inherit = 'event.event'
    
    def google_map_img(self, cr, uid, ids, zoom=12, width=400, height=298, context=None):
        event = self.browse(cr, uid, ids[0], context=context)
        if event.address_id:
            return self.browse(cr, SUPERUSER_ID, ids[0], context=context).address_id.google_map_img()
        return None

    def google_map_link(self, cr, uid, ids, zoom=12, context=None):
        event = self.browse(cr, uid, ids[0], context=context)
        if event.address_id:
            return self.browse(cr, SUPERUSER_ID, ids[0], context=context).address_id.google_map_link()
        return None 
