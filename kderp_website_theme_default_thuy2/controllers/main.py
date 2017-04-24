# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

#Ke thua class KderpWebsite trong module kderp_website
#Tao trang Project Featured va Project Completed
from openerp.addons.kderp_website.controllers.main import KderpWebsite

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