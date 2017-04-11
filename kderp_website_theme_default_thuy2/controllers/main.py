# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

#Ke thua class KderpWebsite trong module kderp_website
#Tao trang Project Ongoing va Project Completed
from openerp.addons.kderp_website.controllers.main import KderpWebsite

class ExtendKderpWebsite(KderpWebsite):
	post_limit = 9
	@http.route(['/pj/ongoing','/pj/ongoing/page/<int:page>'],  auth='public', website=True)
	def kdvn_pj_ongoing(self, page=1 , pager_url="/pj/ongoing"):
		posts = http.request.env['blog.post'].search([('blog_id', '=', 'Project Ongoing')])
		list_posts = posts[(page - 1) * self.post_limit:page * self.post_limit]
		pager = request.website.pager(
			url=pager_url,
			page=page,
			total=len(posts),
			step=self.post_limit
			)
		return http.request.render('kderp_website_theme_default_thuy2.page_pj_ongoing', {'posts': list_posts, 'pager': pager,})
		
	@http.route(['/pj/completed','/pj/completed/page/<int:page>'], auth='public', website=True)
	def kdvn_pj_completed(self, page=1 , pager_url="/pj/completed"):
		posts = http.request.env['blog.post'].search([('blog_id', '=', 'Project Completed')])
		list_posts = posts[(page - 1) * self.post_limit:page * self.post_limit]
		pager = request.website.pager(
			url=pager_url,
			page=page,
			total=len(posts),
			step=self.post_limit
			)
		return http.request.render('kderp_website_theme_default_thuy2.page_pj_completed', {'posts': list_posts, 'pager': pager,})