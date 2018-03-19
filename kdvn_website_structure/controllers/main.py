# -*- coding: ascii -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from itertools import groupby
from lxml import etree
import werkzeug
import mimetypes
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, time


from odoo import api, fields, models
from odoo import tools
from odoo import fields, http, _

from odoo.addons.website.models import website
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.tools import pycompat

from odoo.addons.website.controllers.backend import WebsiteBackend

_logger = logging.getLogger(__name__)
class View(models.Model):
	_inherit = "ir.ui.view"
	
	@api.multi
	def render(self, values=None, engine='ir.qweb'):
		major_works = self.env['ir.config_parameter'].sudo().get_param('major_works')
		es_blog = self.env['ir.config_parameter'].sudo().get_param('es_blog')
		ms_blog = self.env['ir.config_parameter'].sudo().get_param('ms_blog')
		introduction = self.env['ir.config_parameter'].sudo().get_param('introduction')
		resources_download = self.env['ir.config_parameter'].sudo().get_param('resources_download')
		announcements = self.env['ir.config_parameter'].sudo().get_param('announcements')
		announcements_alert = self.env['ir.config_parameter'].sudo().get_param('announcements_alert')
		media = self.env['ir.config_parameter'].sudo().get_param('media')
		resources_download = self.env['ir.config_parameter'].sudo().get_param('resources_download')
		
		works = request.env['blog.post'].search([('blog_id','=',major_works)], offset=0)
		intros = request.env['blog.post'].search([('blog_id','=',introduction)], offset=0)
		news = request.env['blog.post'].search([('blog_id.categories_news', '=', True)],order = "priority desc, sequence desc", offset=0)
		news_e = request.env['blog.post'].search([('blog_id','=',es_blog)], offset=0)
		news_m = request.env['blog.post'].search([('blog_id','=',ms_blog)], offset=0)
		kdvn_file = request.env['blog.post'].search([('blog_id', '=', media),('name','=',resources_download)], offset=0, limit=2)	
		announcements = request.env['blog.post'].search([('blog_id', '=', announcements), ('tag_ids.name', '=', announcements_alert)], offset=0, limit=2)
		announcements = set(j for j in announcements if j.create_date >= (datetime.today() - relativedelta(days=j.relative_date)).strftime('%Y-%m-%d'))

		kdvn_info = {'kdvn_works':works,
					'kdvn_intros':intros,
					'kdvn_news':news,
					'kdvn_news_e':news_e,
					'kdvn_news_m':news_m,
					'kdvn_file':kdvn_file,
					'anns':announcements,
					}
		
		if not values:
			values = dict()
		values.update(kdvn_info)
		return super(View, self).render(values, engine=engine)	        

# class AlertOff(http.Controller):
# 	@http.route("/alert_off/<int:id>", auth="public")
# 	def alert_off(self, id):
# 		""" Stop showing alert having the id"""
# 		http.request.httpsession['alert_off_' + str(id)] = True
# 		return http.local_redirect("/")	
		
class KderpWebsite(http.Controller):
	#download file
	_post_per_page = 6
	@http.route('/website/image/<model>/<id>/<field>/<name>', auth='public', website=True)
	def kdvn_show_attach_file(self, model, id, field, name):
		"""
			Return raw data of attachment as well as trying to guest
			mimetype of the attachment: mostly being used for showing pdf file
			TODO: this just temporary solved pdf file, there will be more cases have to take care of
		"""
		response = werkzeug.wrappers.Response()
		data = http.request.env['ir.attachment'].search([('id','=',id.split('_')[0])])
		response.data = data[field].decode('base64')
		file_ext = data.name[-4:]
		response.mimetype= mimetypes.types_map[file_ext]
		return response
	
	def kdvn_file_library(self, post_id, page, pager_url, template=['kdvn_website_structure.kdvn_str_files', 'website.homepage']):
		"""
			Handling posts that manage attachments as media:
			- Images
			- Attached Files
			- Video
		"""
		post = http.request.env['blog.post'].search([('id', '=', post_id)])
		file_ids = post.img_url_ids
		files = file_ids[(page - 1) * self._post_per_page:page * self._post_per_page]

		pager = request.website.pager(
			url=pager_url,
			page=page,
			total=len(file_ids),
			step=self._post_per_page
		)
		return http.request.render(template, {
			'files': files,
			'pager': pager,
			'post': post
		})
		
	@http.route(['/kdvn/images', '/kdvn/images/page/<int:page>'], website=True)
	def kdvn_image_library(self, page=1):
		env = request.env(context=dict(request.env.context))
		"""
			Keep KINDEN VIETNAM images
		"""
		media = env['ir.config_parameter'].sudo().get_param('media')
		images_library = env['ir.config_parameter'].sudo().get_param('images_library')
		post = http.request.env['blog.post'].search([('blog_id','=',media),('name','=',images_library)])
		return self.kdvn_file_library(post.id, page, '/kdvn/images', 'kdvn_website_structure.kdvn_str_files')

	@http.route(['/kdvn/download', '/kdvn/download/page/<int:page>'], auth='public', website=True)
	def kdvn_download(self, page=1):
		env = request.env(context=dict(request.env.context))
		media = env['ir.config_parameter'].sudo().get_param('media')
		resources_download = env['ir.config_parameter'].sudo().get_param('resources_download')
		post = http.request.env['blog.post'].search([('blog_id','=',media),('name','=',resources_download)])
		return self.kdvn_file_library(post.id, page, '/intro/download','kdvn_website_structure.kdvn_str_files')
		
	#Su dung chung cho cac trang News, Electrical va Mechanical
	post_limit = 9	
	def kdvn_posts(self, blog_name_list=[], post_ids=[], page_url='/', page=1, template=['kdvn_website_structure.kdvn_str_news_post', 'kdvn_website_structure.kdvn_str_news_list_posts']):
		env = request.env(context=dict(request.env.context))
		"""Getting all posts of blog(s) to prepare to show
		- If only 1 post return, show the post
		- If more than 1 post return, list these posts
			+ Also handle pager
			+ Can use website_blog: however rewrite to study
		"""
		es_blog = env['ir.config_parameter'].sudo().get_param('es_blog')
		ms_blog = env['ir.config_parameter'].sudo().get_param('ms_blog')
		announcements = env['ir.config_parameter'].sudo().get_param('announcements')
		ffacts = env['ir.config_parameter'].sudo().get_param('ffacts')
		announcements = http.request.env['blog.post'].search([('blog_id', '=', announcements)])
		funfacts = http.request.env['blog.post'].search([('blog_id','=',ffacts)])
		if post_ids:
			search_domain = [('id', 'in', post_ids)]
		else:
			search_domain = []
			if blog_name_list == []:
				search_domain = [('blog_id.categories_news', '=', True)]
			else :				
				for blog_name in blog_name_list:
					search_domain +=[('blog_id','in',blog_name_list)]
				#Add or condition to the search domain
				if len(search_domain) -1 :
					search_domain.insert(0, '|' * (len(search_domain)-1))
		
		result = http.request.env['blog.post'].search(search_domain)
		if len(result) == 1:
			# Return only one post
			return http.request.render(template[0],{'post':result})
		elif len(result) > 1:
			# Return posts -> list posts
			# Handler pager
			pager = request.website.pager(
				url = page_url,
				page = page,
				total = len(result),
				step = self._post_per_page
			)
			#limit and offset result
			result = http.request.env['blog.post'].search(search_domain, offset=(page-1)*self._post_per_page, limit=self._post_per_page)
			return http.request.render(template[1],{
				'posts': result,
				'pager': pager,
				'announcements': announcements,
				'ffacts': funfacts,
			})
	
	@http.route(['/<submenu>/news', '/<submenu>/news/page/<int:page>'], auth='public', website=True)
	def kdvn_list_posts(self, page=1, submenu='', blog_name_list=[]):
		env = request.env(context=dict(request.env.context))
		"""Showing KDVN News, blog based on route header"""
		es_blog = env['ir.config_parameter'].sudo().get_param('es_blog')
		ms_blog = env['ir.config_parameter'].sudo().get_param('ms_blog')
		submenu_dic = {
			'all':[],
			'es':[es_blog],
			'ms':[ms_blog]          
			}
		if (submenu_dic.keys() == 'all') or (submenu not in submenu_dic.keys()):
			blog_name_list = []
		else:
			blog_name_list = submenu_dic[submenu]
		url = '/' + submenu + '/news'
		return self.kdvn_posts(blog_name_list, [], url, page)
		
	@http.route(['/<submenu>/news/<model("blog.post"):post>','/<submenu>/news/page/<int:page>/<model("blog.post"):post>'], auth='public', website=True)
	def kdvn_show_post(self, post, submenu, page=1):
		"""Showing post content"""
		return self.kdvn_posts([], [post.id])

	#page Kinden Vietnam
	@http.route(['/intro/kdvn',
				'/intro/kdvn/<model("blog.post"):post>'
				], auth='public', website = True)
	def kdvn_intro_post(self, post=None, **kw):
		env = request.env(context=dict(request.env.context))
		introduction = env['ir.config_parameter'].sudo().get_param('introduction')
		domain = [('blog_id', '=', introduction)]
		posts = http.request.env['blog.post'].search(domain, order="sequence asc")
		if post:           
			pager_url = "/intro/kdvn"		
			domain += [('id', '=', int(post))]
		posts_detail = http.request.env['blog.post'].search(domain, order="sequence asc")		
		return http.request.render('kdvn_website_structure.kdvn_str_intro_kdvn',{'posts':posts, 'posts_detail':posts_detail})
	
	#page Certificates
	@http.route(['/intro/certificates'], auth="public", website=True)
	def kdvn_certificates(self, **kw):
		env = request.env(context=dict(request.env.context))
		certificates = env['ir.config_parameter'].sudo().get_param('certificates')
		posts = http.request.env['blog.post'].search([('blog_id', '=', certificates)], order="sequence asc")
		return http.request.render('kdvn_website_structure.kdvn_str_certificates', {'posts': posts})
		
	#page Contactus
	@http.route('/intro/contactus', auth='public', website=True)
	def kdvn_contacts(self, **kw):
		env = request.env(context=dict(request.env.context))
		"""Showing all KDVN contacts: offices and site offices"""
		partner_office = env['ir.config_parameter'].sudo().get_param('partner_office')
		partner_site_office = env['ir.config_parameter'].sudo().get_param('partner_site_office')
		offices = http.request.env['res.partner'].search([('category_id.name','=',partner_office)])
		sites = http.request.env['res.partner'].search([('category_id.name','=',partner_site_office)])
		return http.request.render('kdvn_website_structure.kdvn_str_contacts',{
			'offices': offices,
			'sites': sites
		})
	
	#page Term of Use
	@http.route('/intro/termofuse', auth='public', website=True)
	def termofuse(self, **kw):
		env = request.env(context=dict(request.env.context))
		termofuse = env['ir.config_parameter'].sudo().get_param('termofuse')
		posts = http.request.env['blog.post'].search([('blog_id', '=', termofuse)], order="sequence asc")
		return http.request.render('kdvn_website_structure.kdvn_str_termofuse', {'posts': posts})
		
	#page Project
	@http.route(['/prj/completed','/prj/completed/page/<int:page>'], auth='public', website=True)
	def kdvn_prj_completed(self,page=1,url="/prj/completed", filter=[],template='',type='all',area='all', year='all', category='all',**searches):
		env = request.env(context=dict(request.env.context))
		projects_completed = env['ir.config_parameter'].sudo().get_param('projects_completed')
		return self.send_prj(
							page=page,
							url=url,
							filter=[('blog_id', '=', projects_completed)], 
							template='kdvn_website_structure.kdvn_str_prj_completed', 
							prj_type=type, prj_area=area, prj_year=year, prj_category=category
							)	
	#Menu trai cho trang Projects 
	def send_prj(self,page=1,url='/', filter=[], template="", prj_type='all', prj_area='all', prj_year='all', prj_category='all', **searches):		
		cr, uid, context = request.cr, request.uid, request.context
		#blog_post_obj = request.registry['blog.post']	
		# type_obj = request.registry['kdvn.post.prj.type']
		# area_obj = request.registry['kdvn.post.prj.area']
		# year_obj = request.registry['kdvn.post.prj.year']
		# category_obj = request.registry['kdvn.post.prj.categ']	
		blog_post_obj = request.env['blog.post']	
		type_obj = request.env['kdvn.post.prj.type']
		area_obj = request.env['kdvn.post.prj.area']
		year_obj = request.env['kdvn.post.prj.year']
		category_obj = request.env['kdvn.post.prj.categ']
		
		searches.setdefault('type', prj_type)
		searches.setdefault('area', prj_area)
		searches.setdefault('year', prj_year)
		searches.setdefault('category', prj_category)		
		list_years = http.request.env['kdvn.post.prj.year'].search([],order='code desc', limit=4)
		list_areas = http.request.env['kdvn.post.prj.area'].search([])
		list_types = http.request.env['kdvn.post.prj.type'].search([])
		list_categorys = http.request.env['kdvn.post.prj.categ'].search([])		
		domain_search = {}
		# search domains		
		if searches["type"] != 'all':
			current_type = type_obj.browse(int(searches['type']))
			domain_search["type"] = [("prj_type_id", "=", int(searches["type"]))]
		if searches["area"] != 'all':
			current_area = area_obj.browse(int(searches['area']))
			domain_search["area"] = [("prj_area_id", "=", int(searches["area"]))]			
		# search domain year
		var_list_years = []
		for var_l in list_years:
			var_list_years.append(var_l.name)
		if searches["year"] not in ['all','less_than']:
			current_year = year_obj.browse(int(searches['year']))
			domain_search["year"] = [("prj_year_id", "=", int(searches["year"])) ]
		if searches["year"] =="less_than":
			domain_search["year"] = [("prj_year_id", "not in", var_list_years)]			
		if searches["category"] != 'all':
			current_category = category_obj.browse(int(searches['category']))
			domain_search["category"] = [("prj_categ_id", "=", int(searches["category"]))]			
		def dom_without(without):
			domain = filter
			for key, search in domain_search.items():
				if key != without:
					domain += search
			return domain
		# count by domains without self search
		domain = dom_without('type')
		types = blog_post_obj.read_group( 
								domain, 
								fields=["id", "prj_type_id"],
								groupby="prj_type_id",
								orderby="prj_type_id", 
								)
		types.insert(0, {
			'prj_type_id': ("all", _("All Categories"))
		})		
		domain = dom_without('area')
		areas = blog_post_obj.read_group(domain, fields=["id", "prj_area_id"],groupby="prj_area_id", orderby="prj_area_id")
		areas.insert(0, {
			'prj_area_id': ("all", _("All Area"))
		})		
		domain = dom_without('year')
		years = blog_post_obj.read_group(domain, fields=["id", "prj_year_id"],groupby="prj_year_id", orderby="prj_year_id")
		years.insert(0, {
			'prj_year_id': ("all", _("All Year"))			
		})
		years.insert(0, {
			'prj_year_id': ("less_than", _("Less Than"))
		})		
		domain = dom_without('category')
		categorys = blog_post_obj.read_group(domain, fields=["id", "prj_categ_id"], groupby="prj_categ_id", orderby="prj_categ_id")
		categorys.insert(0, {
			'prj_categ_id': ("all", _("All Categories"))
		})		
		step = 9  # Number of Project per page
		blog_post_count = blog_post_obj.search(dom_without("none"), count=True)
		pager = request.website.pager(
			url= url,
			url_args={ 'area': searches.get('area'), 'type': searches.get('type'), 'category': searches.get('category'),'year': searches.get('year'), },
			total=blog_post_count,
			page=page,
			step=step,
			scope=5)
		obj_ids = blog_post_obj.search(dom_without("none"), limit=step, offset=pager['offset'])
		blog_post_ids = obj_ids
		values = {
			'posts': blog_post_ids,
			'types': types,
			'areas': areas,
			'years': years,
			'categorys': categorys,			
			'list_areas': list_areas,
			'list_types': list_types,
			'list_years': list_years,
			'list_categorys': list_categorys,
			'pager': pager,
			'searches': searches,
			'search_path': "?%s" % werkzeug.url_encode(searches),
			}
		return request.render(template, values)