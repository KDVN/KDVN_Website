# -*- coding: utf-8 -*-
import openerp
import werkzeug
import mimetypes

from openerp import http
from openerp import SUPERUSER_ID

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.http import request

from openerp.osv import orm, osv
from openerp import models, fields, api

from openerp.addons.website.models import website
	
class kdvn_website_config_settings(osv.osv_memory):
	"""
		Ghi du lieu vao module website
	"""
	_name = 'kdvn.website.config.settings'
	_inherit = 'res.config.settings'
	
	_columns = {
		'major_works': openerp.osv.fields.char('Major Works', help="Categories 'Major Works' to add images to slice show homepage"),
		'es_blog': openerp.osv.fields.char('Electrical Systems', help="Categories 'Electrical Systems' to add news Eletrical to page Electrical System"),
		'ms_blog': openerp.osv.fields.char('Mechanical Systems', help="Categories 'Mechanical Systems' to add news Mechanical to page Mechanical System"),
		'announcements': openerp.osv.fields.char('Announcement', help="Categories 'Announcement' to add announcement to menu right in pages news"),
		'announcements_alert': openerp.osv.fields.char('Announcement Alert'),
		'ffacts': openerp.osv.fields.char('Fun Fact', help="Categories 'Fun Fact' to add fun fact to menu right in pages news"),
		'introduction': openerp.osv.fields.char('Introduction', help="Categories 'Introduction' to add information of company to in pages Kinden Vietnam"),
		'certificates': openerp.osv.fields.char('Certificates', help="Categories 'Certificates' to add information of certificates to in pages Certificates"),
		'partner_office': openerp.osv.fields.char('Partner Office', help="Contact Tags 'KDVN_Office' to filter information main Office res_partner in pages Contact us and show footer"),
		'partner_site_office': openerp.osv.fields.char('Partner Site Office', help="Contact Tags 'KDVN_Site_Office' to filter information sub Office res_partner in pages Contact us"),
		'termofuse': openerp.osv.fields.char('Termofuse', help="Categories 'Termofuse' to add information of termofuse to in pages Termofuse"),
		'projects_featured': openerp.osv.fields.char('Projects Featured', help="Categories 'Projects Featured' to add information of projects featured to in pages Projects Featured"),
		'projects_completed': openerp.osv.fields.char('Projects Completed', help="Categories 'Projects Completed' to add information of projects completed to in pages Projects Completed"),
		'media': openerp.osv.fields.char('Media'),
		'images_library': openerp.osv.fields.char('Images Library'),
		'resources_download': openerp.osv.fields.char('Resources Download'),
		'google_map_api_kdvn_key': openerp.osv.fields.char('Google Map Api Kdvn Key'),
	}
	
	def create(self, cr, uid, vals, context=None):
		config_id = super(kdvn_website_config_settings, self).create(cr, uid, vals, context=context)
		self.write(cr, uid, config_id, vals, context=context)
		return config_id
	
	def set_config_kdvn_website_theme(self, cr, uid, ids, context=None):
		config = self.browse(cr, uid, ids[0], context)
		website = self.pool.get('website').browse(cr, uid, uid)
		website.write({
						'major_works': config.major_works,
						'es_blog': config.es_blog,
						'ms_blog': config.ms_blog,
						'announcements': config.announcements,
						'announcements_alert': config.announcements_alert,
						'ffacts': config.ffacts,
						'introduction': config.introduction,						
						'certificates': config.certificates,
						'partner_office': config.partner_office,
						'partner_site_office': config.partner_site_office,
						'termofuse': config.termofuse,
						'projects_featured': config.projects_featured,
						'projects_completed': config.projects_completed,
						'media': config.media,
						'images_library': config.images_library,
						'resources_download': config.resources_download,
						'google_map_api_kdvn_key': config.google_map_api_kdvn_key
					})
	_defaults = {		
		'major_works': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).major_works,
		'es_blog': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).es_blog,
		'ms_blog': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).ms_blog,
		'announcements': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).announcements,
		'announcements_alert': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).announcements_alert,
		'ffacts': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).ffacts,
		'introduction': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).introduction,
		'certificates': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).certificates,
		'partner_office': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).partner_office,
		'partner_site_office': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).partner_site_office,
		'termofuse': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).termofuse,
		'projects_featured': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).projects_featured,
		'projects_completed': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).projects_completed,
		'media': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).media,
		'images_library': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).images_library,
		'resources_download': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).resources_download,
		'google_map_api_kdvn_key': lambda self, cr, uid, context:self.pool.get('website').browse(cr, uid, uid, context).google_map_api_kdvn_key,
	}	
		
class website(osv.osv):
	"""
		Them cac truong trong module website
		Cac truong duoc dung de lam dieu kien de xuat hien du lieu tren website
		Co the cau hinh du lieu cac truong theo duong dan Setting > Configuration > Kdvn Website Setting
	"""
	_name = "website" 
	_inherit = "website"
    
	_columns = {
		'major_works': openerp.osv.fields.char('Major Works'),
		'es_blog': openerp.osv.fields.char('Electrical Systems'),
		'ms_blog': openerp.osv.fields.char('Mechanical Systems'),
		'announcements': openerp.osv.fields.char('Announcement'),
		'announcements_alert': openerp.osv.fields.char('Announcement Alert'),
		'ffacts': openerp.osv.fields.char('Fun Fact'),
		'introduction': openerp.osv.fields.char('Introduction'),
		'certificates': openerp.osv.fields.char('Certificates'),
		'partner_office': openerp.osv.fields.char('Partner Office'),
		'partner_site_office': openerp.osv.fields.char('Partner Site Office'),
		'termofuse': openerp.osv.fields.char('Termofuse'),
		'projects_featured': openerp.osv.fields.char('Projects Featured'),
		'projects_completed': openerp.osv.fields.char('Projects Completed'),
		'google_map_api_kdvn_key': openerp.osv.fields.char('Google Map Api Kdvn Key'),
		#Media and Download
		'media': openerp.osv.fields.char('Media'),
		'images_library': openerp.osv.fields.char('Images Library'),
		'resources_download': openerp.osv.fields.char('Resources Download'),
	}
	_defaults = {
		'major_works': 'Major Works',
		'es_blog': 'Electrical Systems',
		'ms_blog': 'Mechanical Systems',
		'announcements': 'Announcement',
		'announcements_alert': 'Announcement Alert',
		'ffacts': 'Fun Fact',
		'introduction': 'Introduction',
		'certificates': 'Certificates',
		'partner_office': 'KDVN_Office',
		'partner_site_office': 'KDVN_Site_Office',
		'termofuse': 'Termofuse',
		'projects_featured': 'Projects Featured',	
		'projects_completed': 'Projects Completed',
		'media': 'Media',
		'images_library': 'Images Library',
		'resources_download': 'Resources Download',
		
	}

	

