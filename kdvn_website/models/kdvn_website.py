# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import random
import werkzeug

from odoo import api, models, fields, _
from odoo.tools.translate import html_translate
from odoo.tools import html2plaintext


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
	
class KdvnBlogBlog(models.Model):
	_inherit = 'blog.blog'

	blogpost_ids = fields.One2many('blog.post', 'blog_id', string="Blog Posts")
	categories_news = fields.Boolean(string="Categories News", default=False)
	
class KdvnBlogTag(models.Model):
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
	
class KdvnBlogPost(models.Model):
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
	
	# @api.one
	# def copy(self, default=None):
		# default = dict(default or {})
		# default.update({
			# 'sequence': 0
		# })
		# return super(KdvnBlogPost, self).copy(default)
class WebsiteMenu(models.Model):
	"""
		Them icon de hien thi ra menu website
	"""
	_inherit = 'website.menu'

	fa_icon = fields.Char('Font Awesome Icon', help='Given icon must appear on the left of menu label.')
	divider = fields.Boolean('Divider', default=False)
	divider_text = fields.Char('Divider Text', translate=True)

#Partner
def urlplus(url, params):
	return werkzeug.Href(url)(params or None)
class Partner(models.Model):
	_inherit = 'res.partner'
	
	contact_website = fields.Boolean(string="Contact Website", default=False)
	position_x = fields.Char('Position X')
	position_y = fields.Char('Position Y')
	
	@api.multi
	def google_map_img(self, zoom=10, width=298, height=298):
		google_maps_api_key = self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
		if not google_maps_api_key:
			return False		
		#Neu co x, y thi center se dung toa do theo cau truc: "center": "x,y"
		#Neu khong co thi lay theo dia chi
		if self.position_x and self.position_y:
			center = self.position_x+','+self.position_y
		else:
			center = '%s, %s %s, %s' % (self.street or '', self.city or '', self.zip or '', self.country_id and self.country_id.name_get()[0][1] or '')
		params = {
			'center': center,
			'size': "%sx%s" % (height, width),
			'zoom': zoom,
			'sensor': 'false',
			'key': google_maps_api_key,
		}
		#Decorrate markers
		#TODO: customized icon
		params["markers"] = 'color:green|label:K|' + params["center"]
		return urlplus('//maps.googleapis.com/maps/api/staticmap', params)
	@api.multi
	def google_map_link(self, zoom=10):
		params = {
			'q': '%s, %s %s, %s' % (self.street or '', self.city or '', self.zip or '', self.country_id and self.country_id.name_get()[0][1] or ''),
			'z': zoom,
		}
		return urlplus('https://maps.google.com/maps', params)