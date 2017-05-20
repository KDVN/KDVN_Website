import openerp
from openerp import http
from openerp.osv import orm, osv
from openerp import models, fields, api

from openerp import SUPERUSER_ID

import werkzeug

from openerp.addons.website.models.website import urlplus


class view(osv.osv):
    """
     Modify render method to add KDVN information to the homepage
     Cac thong tin tra ve variable values o day se xuat hien o tat ca cac page cua Website
     Nen han che de do bi nang va do ri thong tin khong can thiet
    """
    _inherit = "ir.ui.view"

    @api.cr_uid_ids_context
    def render(self, cr, uid, id_or_xml_id, values=None, engine='ir.qweb', context=None):
        def _search_browse(search_domain, **kwargs):
            """
            :param search_domain: list of search sets
            :return: recordsets
            """
            # Search for tag_ids.name in search domain
            post_tags_not_search = filter(lambda s: s[0] == 'tag_ids.name' and s[1] == 'not in', search_domain)
            if post_tags_not_search:
                # Modify search_domain accordingly
                post_ids_not_tags = self.pool['blog.post'].search(cr, uid, [('tag_ids.name', 'in', post_tags_not_search[0][2])])
                search_domain.remove(post_tags_not_search[0])
                search_domain.append(('id', 'not in', post_ids_not_tags))

            post_ids = self.pool['blog.post'].search(cr, uid, search_domain, **kwargs)
            #Them context=context de hien thi phan translate ra homepage
            return self.pool['blog.post'].browse(cr, uid, post_ids, context=context)

        qa_tag_list = ['KinQ News','KinVQ News']
        news_list = ['General News', 'IT', 'Quality Safety Assurance', 'Electrical Systems', 'Mechanical Systems']

        # KDVN hot news
        news = _search_browse([('blog_id', 'in', news_list), ('tag_ids.name', 'not in', qa_tag_list)], offset=0, limit=8)
        # news_ids = self.pool['blog.post'].search(cr, uid, [('blog_id', 'in', news_list), '!', ('tag_ids.name', 'in', qa_tag_list)], offset=0, limit=8)
        # news = self.pool['blog.post'].browse(cr, uid, news_ids)

        # KDVN Electrical | Mechanical | QA news
        news_e = _search_browse([('blog_id', '=', 'Electrical Systems')], offset=0, limit=2)
        news_m= _search_browse([('blog_id', '=', 'Mechanical Systems')], offset=0, limit=2)
        news_q = _search_browse([('blog_id', '=', 'Quality Safety Assurance'), ('tag_ids.name', 'not in', qa_tag_list)], offset=0, limit=2)

        # KDVN works for
        work_tag = "KDVN_Works"
        works = _search_browse([('tag_ids','=', work_tag)], offset=0)
        work_tag_new = "KDVN_Works_New"
        works_new = _search_browse([('tag_ids','=', work_tag_new)], offset=0)
        
        # KDVN ME (for homepage features)
        me = _search_browse([('blog_id','=','Introduction'),('name', 'in', ['Mechanical Systems', 'Electrical Systems'])], order="name")
        #Hien thi file download ra homepage
        kdvn_file = _search_browse([('blog_id', '=', 'Media'),('name','=','Resources Download')], offset=0, limit=4)

        kdvn_info = {"kdvn_news":news, "kdvn_works":works, "kdvn_me": me, "kdvn_news_e":news_e, "kdvn_news_m":news_m, "kdvn_news_q":news_q, 'kdvn_file':kdvn_file,
                     "kdvn_works_new":works_new,}

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
		
class Partner(models.Model):
    #TODO: Central management for API keys
    _inherit = 'res.partner'
    def google_map_img(self, cr, uid, ids, zoom=18, width=298, height=298, context=None):
    
        partner = self.browse(cr, uid, ids[0], context=context)
        params = {
            'center': '%s, %s %s, %s' % (partner.street or '', partner.city or '', partner.zip or '', partner.country_id and partner.country_id.name_get()[0][1] or ''),
            'size': "%sx%s" % (height, width),
            'zoom': zoom,
            'sensor': 'false',
            'key': 'AIzaSyBAH0ggPtUks7WjlgAM_VkNAhP6Mqy_F48'
        }
        return urlplus('//maps.googleapis.com/maps/api/staticmap' , params)

	name = fields.Char(string="Name", translate=True)
	street = fields.Char(string="Address", translate=True)
	street2 = fields.Char(string="Address2", translate=True)
	city = fields.Char(string="City", translate=True)
	
	

	    