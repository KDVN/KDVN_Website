# -*- coding: utf-8 -*-
import openerp
import werkzeug
import mimetypes
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from openerp import http
from openerp import SUPERUSER_ID
from openerp.tools.translate import _

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.http import request

from openerp.osv import orm, osv
from openerp import models, fields, api

from openerp.addons.website.models import website	
from openerp.addons.website_blog.controllers.main import QueryURL

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
			post_ids = self.pool['blog.post'].search(cr, uid, search_domain, **kwargs)           
			return self.pool['blog.post'].browse(cr, uid, post_ids, context=context)
			
		#Lay gia tri tu Kdvn Website Setting
		major_works = self.pool['website'].browse(cr, uid, 1, context=context).major_works
		introduction = self.pool['website'].browse(cr, uid, 1, context=context).introduction
		media = self.pool['website'].browse(cr, uid, 1, context=context).media
		resources_download = self.pool['website'].browse(cr, uid, 1, context=context).resources_download
		es_blog = self.pool['website'].browse(cr, uid, 1, context=context).es_blog
		ms_blog = self.pool['website'].browse(cr, uid, 1, context=context).ms_blog
		announcements = self.pool['website'].browse(cr, uid, 1, context=context).announcements
		announcements_alert = self.pool['website'].browse(cr, uid, 1, context=context).announcements_alert
		
		#Hien cac anh trong Major Works ra slice show trong homepage
		works = _search_browse([('blog_id','=',major_works)], offset=0)		
		#Hien thi tat cac tin tuc ra Homepage		
		news = _search_browse([('blog_id.categories_news', '=', True)],order = "priority desc, sequence desc", offset=0)
		# KDVN Electrical | Mechanical : Homepage
		news_e = _search_browse([('blog_id','=',es_blog)], offset=0)		
		news_m = _search_browse([('blog_id','=',ms_blog)], offset=0)		
		#Hien thi intro: thong tin cac trang kinden vietnam ra Homepage
		intros = _search_browse([('blog_id', '=', introduction)],order = "priority desc, sequence desc", offset=0)
		#Hien thi file download ra Homepage
		kdvn_file = _search_browse([('blog_id', '=', media),('name','=',resources_download)], offset=0, limit=2)	
		#Hien thi Announcment Alert ra tat ca cac trang
		announcements = _search_browse([('blog_id', '=', announcements), ('tag_ids.name', '=', announcements_alert)], offset=0, limit=2)
		announcements = set(j for j in announcements if j.create_date >= (datetime.today() - relativedelta(days=j.relative_date)).strftime('%Y-%m-%d'))

		kdvn_info = {'kdvn_news':news, 
					'kdvn_works':works, 
					'kdvn_file':kdvn_file,
					'kdvn_intros':intros,
					'kdvn_news_e':news_e,
					'kdvn_news_m':news_m,
					'anns':announcements,
					
					}
		if not values:
			values = dict()
		values.update(kdvn_info)
		return super(view, self).render(cr, uid, id_or_xml_id, values=values, engine=engine, context=context)	
		
class AlertOff(http.Controller):
	@http.route("/alert_off/<int:id>", auth="public")
	def alert_off(self, id):
		""" Stop showing alert having the id"""
		http.request.httpsession['alert_off_' + str(id)] = True
		return http.local_redirect("/")	
		
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
		"""
			Keep KINDEN VIETNAM images
		"""
		media = request.website.media
		images_library = request.website.images_library
		post = http.request.env['blog.post'].search([('blog_id','=',media),('name','=',images_library)])
		return self.kdvn_file_library(post.id, page, '/kdvn/images', 'kdvn_website_structure.kdvn_str_files')

	@http.route(['/kdvn/download', '/kdvn/download/page/<int:page>'], auth='public', website=True)
	def kdvn_download(self, page=1):
		media = request.website.media
		resources_download = request.website.resources_download
		post = http.request.env['blog.post'].search([('blog_id','=',media),('name','=',resources_download)])
		return self.kdvn_file_library(post.id, page, '/intro/download','kdvn_website_structure.kdvn_str_files')
		
	#Su dung chung cho cac trang News, Electrical va Mechanical
	post_limit = 9	
	def kdvn_posts(self, blog_name_list=[], post_ids=[], page_url='/', page=1, template=['kdvn_website_structure.kdvn_str_news_post', 'kdvn_website_structure.kdvn_str_news_list_posts']):
		"""Getting all posts of blog(s) to prepare to show
		- If only 1 post return, show the post
		- If more than 1 post return, list these posts
			+ Also handle pager
			+ Can use website_blog: however rewrite to study
		"""
		es_blog = request.website.es_blog
		ms_blog = request.website.ms_blog
		announcements = request.website.announcements
		ffacts = request.website.ffacts
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
		"""Showing KDVN News, blog based on route header"""
		es_blog = request.website.es_blog
		ms_blog = request.website.ms_blog
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
		introduction = request.website.introduction
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
		certificates = request.website.certificates
		posts = http.request.env['blog.post'].search([('blog_id', '=', certificates)], order="sequence asc")
		return http.request.render('kdvn_website_structure.kdvn_str_certificates', {'posts': posts})
		
	#page Contactus
	@http.route('/intro/contactus', auth='public', website=True)
	def kdvn_contacts(self, **kw):
		"""Showing all KDVN contacts: offices and site offices"""
		partner_office = request.website.partner_office
		partner_site_office = request.website.partner_site_office
		offices = http.request.env['res.partner'].search([('category_id.name','=',partner_office)])
		sites = http.request.env['res.partner'].search([('category_id.name','=',partner_site_office)])
		return http.request.render('kdvn_website_structure.kdvn_str_contacts',{
			'offices': offices,
			'sites': sites
		})
	
	#page Term of Use
	@http.route('/intro/termofuse', auth='public', website=True)
	def termofuse(self, **kw):
		termofuse = request.website.termofuse
		posts = http.request.env['blog.post'].search([('blog_id', '=', termofuse)], order="sequence asc")
		return http.request.render('kdvn_website_structure.kdvn_str_termofuse', {'posts': posts})
		
	#page Project
	@http.route(['/prj/completed','/prj/completed/page/<int:page>'], auth='public', website=True)
	def kdvn_prj_completed(self,page=1,url="/prj/completed", filter=[],template='',type='all',area='all', year='all', category='all',**searches):
		projects_completed = request.website.projects_completed
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
		blog_post_obj = request.registry['blog.post']
		type_obj = request.registry['kdvn.post.prj.type']
		area_obj = request.registry['kdvn.post.prj.area']
		year_obj = request.registry['kdvn.post.prj.year']
		category_obj = request.registry['kdvn.post.prj.categ']		
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
			current_type = type_obj.browse(cr, uid, int(searches['type']), context=context)
			domain_search["type"] = [("prj_type_id", "=", int(searches["type"]))]
		if searches["area"] != 'all':
			current_area = area_obj.browse(cr, uid, int(searches['area']), context=context)
			domain_search["area"] = [("prj_area_id", "=", int(searches["area"]))]			
		# search domain year
		var_list_years = []
		for var_l in list_years:
			var_list_years.append(var_l.name)
		if searches["year"] not in ['all','less_than']:
			current_year = year_obj.browse(cr, uid, int(searches['year']), context=context)
			domain_search["year"] = [("prj_year_id", "=", int(searches["year"])) ]
		if searches["year"] =="less_than":
			domain_search["year"] = [("prj_year_id", "not in", var_list_years)]			
		if searches["category"] != 'all':
			current_category = category_obj.browse(cr, uid, int(searches['category']), context=context)
			domain_search["category"] = [("prj_categ_id", "=", int(searches["category"]))]			
		def dom_without(without):
			domain = filter
			for key, search in domain_search.items():
				if key != without:
					domain += search
			return domain
		# count by domains without self search
		domain = dom_without('type')
		types = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "prj_type_id"], groupby="prj_type_id", orderby="prj_type_id", context=request.context)
		types.insert(0, {
			'prj_type_id': ("all", _("All Categories"))
		})		
		domain = dom_without('area')
		areas = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "prj_area_id"],groupby="prj_area_id", orderby="prj_area_id", context=request.context)
		areas.insert(0, {
			'prj_area_id': ("all", _("All Area"))
		})		
		domain = dom_without('year')
		years = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "prj_year_id"],groupby="prj_year_id", orderby="prj_year_id", context=request.context)
		years.insert(0, {
			'prj_year_id': ("all", _("All Year"))			
		})
		years.insert(0, {
			'prj_year_id': ("less_than", _("Less Than"))
		})		
		domain = dom_without('category')
		categorys = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "prj_categ_id"], groupby="prj_categ_id", orderby="prj_categ_id", context=request.context)
		categorys.insert(0, {
			'prj_categ_id': ("all", _("All Categories"))
		})		
		step = 9  # Number of Project per page
		blog_post_count = blog_post_obj.search(
			request.cr, request.uid, dom_without("none"), count=True,
			context=request.context)
		pager = request.website.pager(
			url= url,
			url_args={ 'area': searches.get('area'), 'type': searches.get('type'), 'category': searches.get('category'),'year': searches.get('year'), },
			total=blog_post_count,
			page=page,
			step=step,
			scope=5)
		obj_ids = blog_post_obj.search(request.cr, request.uid, dom_without("none"), limit=step, offset=pager['offset'],  context=request.context)
		blog_post_ids = blog_post_obj.browse(request.cr, request.uid, obj_ids, context=request.context)
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
		return request.website.render(template, values)
	