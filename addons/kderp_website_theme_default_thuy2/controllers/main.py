# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from openerp import tools
import werkzeug.urls
from werkzeug.exceptions import NotFound

import babel.dates
import time
from openerp.addons.website.models.website import slug

#Ke thua class KderpWebsite trong module kderp_website
#Tao trang Project Featured va Project Completed
from openerp.addons.kderp_website.controllers.main import KderpWebsite
#Ke thua class website_hr_recruitment trong module website_hr_recruitment
from openerp.addons.website_hr_recruitment.controllers.main import website_hr_recruitment

class ExtendKderpWebsite(KderpWebsite):
	@http.route(['/pj/featured', '/pj/featured/page/<int:page>'], type='http', auth="public", website=True)
	def kdvn_pj_featured(self,page=1,url="/pj/featured", filter=[],template='',type='all',area='all', year='all', size='all',**searches):
		return self.send_prj(
							page=page, 
							url=url,
							filter=['|',('blog_id', '=', 'Projects Featured'),('tag_ids','=', 'Project Featured Tags')], 
							template='kderp_website_theme_default_thuy2.page_pj_featured', 
							prj_type=type, prj_area=area, prj_year=year, prj_size=size
							)
							
	@http.route(['/pj/completed','/pj/completed/page/<int:page>'], auth='public', website=True)
	def kdvn_pj_completed(self,page=1,url="/pj/completed", filter=[],template='',type='all',area='all', year='all', size='all',**searches):
		return self.send_prj(
							page=page,
							url=url,
							filter=['|',('blog_id', '=', 'Projects Completed'),('tag_ids','=', 'Project Completed Tags')], 
							template='kderp_website_theme_default_thuy2.page_pj_completed', 
							prj_type=type, prj_area=area, prj_year=year, prj_size=size
							)
							
	def send_prj(self,page=1,url='/', filter=[], template="", prj_type='all', prj_area='all', prj_year='all', prj_size='all', **searches):
		
		cr, uid, context = request.cr, request.uid, request.context
		blog_post_obj = request.registry['blog.post']
		type_obj = request.registry['kderp.blog.post.project.type']
		area_obj = request.registry['kderp.area']
		year_obj = request.registry['kderp.blog.post.year']
		size_obj = request.registry['kderp.blog.post.project.size']
		
		searches.setdefault('type', prj_type)
		searches.setdefault('area', prj_area)
		searches.setdefault('year', prj_year)
		searches.setdefault('size', prj_size)
		
		list_years = http.request.env['kderp.blog.post.year'].search([],order='code desc', limit=4)
		list_areas = http.request.env['kderp.area'].search([])
		list_types = http.request.env['kderp.blog.post.project.type'].search([])
		list_sizes = http.request.env['kderp.blog.post.project.size'].search([])
		
		domain_search = {}
		# search domains		
		if searches["type"] != 'all':
			current_type = type_obj.browse(cr, uid, int(searches['type']), context=context)
			domain_search["type"] = [("type", "=", int(searches["type"]))]
		if searches["area"] != 'all':
			current_area = area_obj.browse(cr, uid, int(searches['area']), context=context)
			domain_search["area"] = [("area_id", "=", int(searches["area"]))]
			
		# search domain year
		var_list_years = []
		for var_l in list_years:
			var_list_years.append(var_l.name)
		if searches["year"] not in ['all','less_than']:
			current_year = year_obj.browse(cr, uid, int(searches['year']), context=context)
			domain_search["year"] = [("project_year_id", "=", int(searches["year"])) ]
		if searches["year"] =="less_than":
			domain_search["year"] = [("project_year_id", "not in", var_list_years)]
			
		if searches["size"] != 'all':
			current_size = size_obj.browse(cr, uid, int(searches['size']), context=context)
			domain_search["size"] = [("size", "=", int(searches["size"]))]
			
		def dom_without(without):
			#domain = [('blog_id', '=', 'Projects Featured')]
			domain = filter
			for key, search in domain_search.items():
				if key != without:
					domain += search
			return domain
		# count by domains without self search
		domain = dom_without('type')
		types = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "type"], groupby="type", orderby="type", context=request.context)
		types.insert(0, {
			'type': ("all", _("All Categories"))
		})
		
		domain = dom_without('area')
		areas = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "area_id"],groupby="area_id", orderby="area_id", context=request.context)
		areas.insert(0, {
			'area_id': ("all", _("All Area"))
		})
		
		domain = dom_without('year')
		years = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "project_year_id"],groupby="project_year_id", orderby="project_year_id", context=request.context)
		years.insert(0, {
			'project_year_id': ("all", _("All Year"))
			
		})
		years.insert(0, {
			'project_year_id': ("less_than", _("Less Than"))
		})
		
		domain = dom_without('size')
		sizes = blog_post_obj.read_group(request.cr, request.uid, domain, ["id", "size"], groupby="size", orderby="size", context=request.context)
		#size_count = blog_post_obj.search(request.cr, request.uid, domain, count=True, context=request.context)
		sizes.insert(0, {
			#'size_count': size_count,
			'size': ("all", _("All Categories"))
		})
		
		step = 9  # Number of events per page
		blog_post_count = blog_post_obj.search(
			request.cr, request.uid, dom_without("none"), count=True,
			context=request.context)
		pager = request.website.pager(
			url= url,
			url_args={ 'area': searches.get('area'), 'type': searches.get('type'), 'size': searches.get('size'),'year': searches.get('year'), },
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
			'sizes': sizes,
			
			'list_areas': list_areas,
			'list_types': list_types,
			'list_years': list_years,
			'list_sizes': list_sizes,

			'pager': pager,
			'searches': searches,
			'search_path': "?%s" % werkzeug.url_encode(searches),
			}
		# import logging
		# _logger = logging.getLogger(__name__)
		# _logger.warning(values['searches'])
		return request.website.render(template, values)

#ke thua class jobs trong module website_hr_recruitment de loc cac recruitment co deadline lon hon ngay hien tai 
class ExtendWebsiteHrRecruitment(website_hr_recruitment):	
	@http.route()
	def jobs(self, country=None, department=None, office_id=None, **kwargs):
		def sd(date):
			return date.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)
		today = datetime.today()
		
		env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
		
		Country = env['res.country']
		Jobs = env['hr.job']

		# List jobs available to current UID
		job_ids = Jobs.search([("date_deadline", ">=", sd(today - relativedelta(days=10)))], order="website_published desc,date_deadline desc,no_of_recruitment desc").ids
		# Browse jobs as superuser, because address is restricted
		jobs = Jobs.sudo().browse(job_ids)

		# Deduce departments and offices of those jobs
		departments = set(j.department_id for j in jobs if j.department_id)
		offices = set(j.address_id for j in jobs if j.address_id)
		countries = set(o.country_id for o in offices if o.country_id)

		# Default search by user country
		if not (country or department or office_id or kwargs.get('all_countries')):
			country_code = request.session['geoip'].get('country_code')
			if country_code:
				countries_ = Country.search([('code', '=', country_code)])
				country = countries_[0] if countries_ else None
				if not any(j for j in jobs if j.address_id and j.address_id.country_id == country):
					country = False

		# Filter the matching one
		if country and not kwargs.get('all_countries'):
			jobs = (j for j in jobs if j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id)
		if department:
			jobs = (j for j in jobs if j.department_id and j.department_id.id == department.id)
		if office_id:
			jobs = (j for j in jobs if j.address_id and j.address_id.id == office_id)

		# Render page
		return request.website.render("website_hr_recruitment.index", {
			'jobs': jobs,
			'countries': countries,
			'departments': departments,
			'offices': offices,
			'country_id': country,
			'department_id': department,
			'office_id': office_id,
		})