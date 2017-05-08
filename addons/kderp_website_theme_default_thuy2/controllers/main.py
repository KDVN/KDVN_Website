# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from openerp import tools

#Ke thua class KderpWebsite trong module kderp_website
#Tao trang Project Featured va Project Completed
from openerp.addons.kderp_website.controllers.main import KderpWebsite
#Ke thua class website_hr_recruitment trong module website_hr_recruitment
from openerp.addons.website_hr_recruitment.controllers.main import website_hr_recruitment

class ExtendKderpWebsite(KderpWebsite):
	post_limit = 9
	@http.route(['/pj/featured','/pj/featured/page/<int:page>'],  auth='public', website=True)
	def kdvn_pj_featured(self, page=1 , pager_url="/pj/featured"):
		posts = http.request.env['blog.post'].search([('blog_id', '=', 'Projects Featured')])
		list_posts = posts[(page - 1) * self.post_limit:page * self.post_limit]
		pager = request.website.pager(
			url=pager_url,
			page=page,
			total=len(posts),
			step=self.post_limit
			)
		return http.request.render('kderp_website_theme_default_thuy2.page_pj_featured', {'posts': list_posts, 'pager': pager,})
		
	@http.route(['/pj/completed','/pj/completed/page/<int:page>'], auth='public', website=True)
	def kdvn_pj_completed(self, page=1 , pager_url="/pj/completed"):
		posts = http.request.env['blog.post'].search([('blog_id', '=', 'Projects Completed')])
		list_posts = posts[(page - 1) * self.post_limit:page * self.post_limit]
		pager = request.website.pager(
			url=pager_url,
			page=page,
			total=len(posts),
			step=self.post_limit
			)
		return http.request.render('kderp_website_theme_default_thuy2.page_pj_completed', {'posts': list_posts, 'pager': pager,})
		
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