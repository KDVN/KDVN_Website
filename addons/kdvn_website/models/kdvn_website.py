import openerp
import time

from openerp.osv import orm, osv, fields
from openerp import models, fields, api, _

import openerp
from openerp import http
from openerp.osv import orm, osv, fields
from openerp import models, fields, api

from openerp.exceptions import AccessError, Warning

from openerp import SUPERUSER_ID

import werkzeug

from openerp.addons.website.models.website import urlplus
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

class KdvnPostPrjYear(models.Model):
	_name = "kdvn.post.prj.year"

	code = fields.Char('Code',size=16,required=True)
	name = fields.Char('Name',size=64,required=True)
	description = fields.Char('Description')	
	
	_sql_constraints = [('code_uniq', 'unique (code)', 'The code of the Kdvn Project Year must be unique !')]
	
class KdvnPostPrjType(models.Model):
	_name = "kdvn.post.prj.type"

	code = fields.Char('Code',size=16,required=True)
	name = fields.Char('Name',size=64,required=True)
	description = fields.Char('Description')
	_sql_constraints = [('code_uniq', 'unique (code)', 'The code of the Kdvn Project Year must be unique !')]

class KdvnPostPrjCateg(models.Model):
	_name = 'kdvn.post.prj.categ'

	sequence = fields.Integer("Seq.")
	name = fields.Char("Name", size=16, required = True, translate=True)
	description = fields.Char("Description", size=128)

	_sql_constraints = [
		('sequence_uniq','unique(sequence)', 'The sequence of the Kdvn Project Categories must be unique !'),
		('name_uniq','unique(name)', 'The name of the Kdvn Project Categories must be unique !')
		]

class KdvnPostPrjArea(models.Model):
	_name = "kdvn.post.prj.area"
	
	code = fields.Char('Code', required=True)
	name = fields.Char('Name',required=True, translate=True)
	
	_sql_constraints = [
		('code_uniq','unique(code)', 'The code of the Kdvn Project Area must be unique !'),
		('name_uniq','unique(name)', 'The name of the Kdvn Project Area must be unique !')
		]
		
class KdvnPostPrjLocation(models.Model):
	_name = "kdvn.post.prj.location"

	name = fields.Char('Name',required=True)
	description = fields.Char('Description')
	area_id = fields.Many2one('kdvn.post.prj.area', 'Area')
	
class KdvnWebsiteMenu(osv.osv):
	"""
	- Adding divider option to menu
	- TODO: How to use both old and new api correctly, ex: fields
	"""
	_inherit = "website.menu"
	_columns = {
		'divider': openerp.osv.fields.boolean('Divider', default=False),
		'divider_text': openerp.osv.fields.char('Divider Text', translate=True)
	}
KdvnWebsiteMenu()

class KdvnNews(models.Model):
	_inherit = 'blog.blog'

	blogpost_ids = fields.One2many('blog.post', 'blog_id', string="Blog Posts")
	categories_news = fields.Boolean(string="Categories News", default=False)
	
class BlogTag(models.Model):
	_inherit = 'blog.tag'
	
	blog_blog_name = fields.Char(string="Blogs", compute='_get_blog_blog_name')
	description = fields.Char(string="Description")
	
	@api.one
	def _get_blog_blog_name(self):
		result = ""
		ids = []
		for blog in self:
			if blog.post_ids:
				for b in blog.post_ids:
					ids.append(b.blog_id.id)
				self.blog_blog_name = str(list(set(ids)))
		blogs = self.env['blog.blog'].search([('id', 'in', list(set(ids)))])
		for blog in blogs:
			result += blog.name+'\n'
		self.blog_blog_name = result  
	
class KdvnPost(models.Model):
	_inherit = 'blog.post'
			
	@api.one
	def _get_img_url_ids(self):
		result = []
		attachments = self.env['ir.attachment'].search([('res_model','=','blog.post'),('res_id','=',self.id)])
		
		for att in attachments:
			result.append(att.id)
		self.img_url_ids = result
		
	#Tu dong dien so sequence	
	@api.onchange('blog_id')
	def do_stuff(self):
		self.env.cr.execute("Select \
								max(bp.sequence)::integer \
							from \
								blog_post bp \
							left join \
								blog_blog bb on bp.blog_id = bb.id \
							where bb.id = %d" % (self.blog_id))
		if self.env.cr.rowcount:
			next_code=str(self.env.cr.fetchone()[0])
			if next_code.isdigit():
				next_code=int(next_code)+1
			else:
				next_code= 1
		else:
			next_code=1			
		if self.blog_id:
			self.sequence = next_code
		
	#Dien nam theo nam 'Completion Date'
	@api.onchange('prj_compl_date', 'prj_year_id')
	def onchange_year(self):
		self.env.cr.execute("select id, code from kdvn_post_prj_year")
		if not self.prj_compl_date:
			self.prj_year_id = None
		else:
			completion_date= datetime.strptime(self.prj_compl_date,"%Y-%m-%d")
			year = completion_date.strftime('%Y')
			for id, code in self.env.cr.fetchall():
				if code == year:
					self.prj_year_id = id
	
	#Dien Area theo Location
	@api.multi
	def onchange_location(self,prj_location_id=False):
		val={}
		if not prj_location_id:
			val={
				'prj_area_id': False
			}
		else:
			location = self.env['kdvn.post.prj.location'].browse(prj_location_id)
			val={
				'prj_area_id': location.area_id.id if location.area_id else False,
			}
		return {'value':val}	
	
	img_url_ids = fields.One2many('ir.attachment', string="Image URLs", compute='_get_img_url_ids')
	summary = fields.Text('Summary', translate=True) 
	sequence = fields.Integer('Sequence')
	priority = fields.Boolean(string='Priority')
	relative_date = fields.Integer(string="Relative Date", size=4)
	
	blog_name = fields.Char(related='blog_id.name')
	prj_compl_date = fields.Date(string='Compl. Date')
	prj_location_id = fields.Many2one('kdvn.post.prj.location', string="Location")
	prj_area_id = fields.Many2one('kdvn.post.prj.area', string="Area")
	prj_year_id = fields.Many2one('kdvn.post.prj.year', string="Years")
	prj_categ_id = fields.Many2one('kdvn.post.prj.categ', string="Category")
	prj_type_id = fields.Many2one('kdvn.post.prj.type', string="Type")
	
	_sql_constraints = [('seqence_blog_id_uniq', 'unique(blog_id, sequence)', 'Two sequence of one category with the same number? Impossible!')]
	
	#Ham duplicate	
	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update({
			'sequence': False
		})
		return super(KdvnPost, self).copy(default)
		
class Partner(osv.Model):
	#TODO: Central management for API keys
	_inherit = 'res.partner'
	def google_map_img(self, cr, uid, ids, zoom=10, width=298, height=298, context=None):
		google_map_api_kdvn_key = self.pool['website'].browse(cr, uid, 1, context=context).google_map_api_kdvn_key
		partner = self.browse(cr, uid, ids[0], context=context)
		
		#Neu co lat, lon thi center se dung toa do theo cau truc: "center": "x,y"
		#Neu khong co thi lay theo dia chi
		if partner.position_x and partner.position_y:
			center = partner.position_x+','+partner.position_y
		else:
			center = '%s,%s%s,%s' % (partner.street or '', partner.city or '', partner.zip or '', partner.country_id and partner.country_id.name_get()[0][1] or '')
		
		params = {
			'center': center,
			'size': "%dx%d" % (height, width),
			'zoom': zoom,
			'sensor': 'false',
			#'key': 'AIzaSyBAH0ggPtUks7WjlgAM_VkNAhP6Mqy_F48'
			'key': google_map_api_kdvn_key
		}
		#Decorrate markers
		#TODO: customized icon
		params["markers"] = 'color:green|label:K|' + params["center"]
		static_map_url = '//maps.googleapis.com/maps/api/staticmap?'
		return urlplus('//maps.googleapis.com/maps/api/staticmap' , params)
	
	def google_map_link(self, cr, uid, ids, zoom=10, context=None):
		partner = self.browse(cr, uid, ids[0], context=context)
		
		if partner.position_x and partner.position_y:
			center = partner.position_x+','+partner.position_y
		else:
			center = '%s,%s%s,%s' % (partner.street or '', partner.city or '', partner.zip or '', partner.country_id and partner.country_id.name_get()[0][1] or '')
			
		params = {
			'q': center,
			'z': zoom,
		}
		return urlplus('https://maps.google.com/maps' , params)
		
	_columns = {
		'position_x':openerp.osv.fields.char('Position X'),
		'position_y':openerp.osv.fields.char('Position Y'),
		'name': openerp.osv.fields.char(string="Name", translate=True),
		'street': openerp.osv.fields.char(string="Address", translate=True),
		'street2': openerp.osv.fields.char(string="Address2", translate=True),
		'city': openerp.osv.fields.char(string="City", translate=True),
		'contact_website': openerp.osv.fields.boolean(string="Contact Website", default=False)
		}
Partner()

	
		