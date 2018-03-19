# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#

from ast import literal_eval

from odoo import api, fields, models
from odoo.exceptions import AccessDenied
	
class KdvnWebsieConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	major_works = fields.Char('Major Works', default='Major Works', help="Categories 'Major Works' to add images to slice show homepage")
	es_blog = fields.Char('Electrical Systems', default='Electrical Systems', help="Categories 'Electrical Systems' to add news Eletrical to page Electrical System")
	ms_blog =  fields.Char('Mechanical Systems', default='Mechanical Systems', help="Categories 'Mechanical Systems' to add news Mechanical to page Mechanical System")
	announcements = fields.Char('Announcement', default='Announcement', help="Categories 'Announcement' to add announcement to menu right in pages news")
	announcements_alert =  fields.Char('Announcement Alert', default='Announcement Alert')
	ffacts =  fields.Char('Fun Fact', default='Fun Fact', help="Categories 'Fun Fact' to add fun fact to menu right in pages news")
	introduction =  fields.Char('Introduction', default='Introduction', help="Categories 'Introduction' to add information of company to in pages Kinden Vietnam")
	certificates =  fields.Char('Certificates', default='Certificates', help="Categories 'Certificates' to add information of certificates to in pages Certificates")
	partner_office =  fields.Char('Partner Office', default='KDVN_Office', help="Contact Tags 'KDVN_Office' to filter information main Office res_partner in pages Contact us and show footer")
	partner_site_office =  fields.Char('Partner Site Office', default='KDVN_Site_Office', help="Contact Tags 'KDVN_Site_Office' to filter information sub Office res_partner in pages Contact us")
	termofuse =  fields.Char('Termofuse', default='Termofuse', help="Categories 'Termofuse' to add information of termofuse to in pages Termofuse")
	projects_featured =  fields.Char('Projects Featured', default='Projects Featured', help="Categories 'Projects Featured' to add information of projects featured to in pages Projects Featured")
	projects_completed =  fields.Char('Projects Completed', default='Projects Completed', help="Categories 'Projects Completed' to add information of projects completed to in pages Projects Completed")
	media =  fields.Char('Media', default='Media')
	images_library =  fields.Char('Images Library', default='Images Library')
	resources_download =  fields.Char('Resources Download', default='Resources Download')
	google_maps_api_key = fields.Char(string='Google Maps API Key')
	
	@api.model
	def get_values(self):
		res = super(KdvnWebsieConfigSettings, self).get_values()
		get_param = self.env['ir.config_parameter'].sudo().get_param
		res.update( 
			major_works=get_param('major_works', default='Major Works'),
			es_blog=get_param('es_blog', default='Electrical Systems'),
			ms_blog=get_param('ms_blog', default='Mechanical Systems'),
			announcements=get_param('announcements', default='Announcement'),
			announcements_alert=get_param('announcements_alert', default='Announcement Alert'),
			ffacts=get_param('ffacts', default='Fun Fact'),
			introduction=get_param('introduction', default='Introduction'),
			certificates=get_param('certificates', default='Certificates'),
			partner_office=get_param('partner_office', default='KDVN_Office'),
			partner_site_office=get_param('partner_site_office', default='KDVN_Site_Office'),
			termofuse=get_param('termofuse', default='Termofuse'),
			projects_featured=get_param('projects_featured', default='Projects Featured'),
			projects_completed=get_param('projects_completed', default='Projects Completed'),
			media=get_param('media', default='Media'),
			images_library=get_param('images_library', default='Images Library'),
			resources_download=get_param('resources_download', default='Resources Download'),
			google_maps_api_key=get_param('google_maps_api_key', default=''),
		)
		return res

	def set_values(self):
		set_param = self.env['ir.config_parameter'].sudo().set_param        
		set_param('major_works', self.major_works)
		set_param('es_blog', self.es_blog)
		set_param('ms_blog', self.ms_blog)
		set_param('announcements', self.announcements)
		set_param('announcements_alert', self.announcements_alert)
		set_param('ffacts', self.ffacts)
		set_param('introduction', self.introduction)
		set_param('certificates', self.certificates)
		set_param('partner_office', self.partner_office)
		set_param('partner_site_office', self.partner_site_office)
		set_param('termofuse', self.termofuse)
		set_param('projects_featured', self.projects_featured)
		set_param('projects_completed', self.projects_completed)
		set_param('media', self.media)
		set_param('images_library', self.images_library)
		set_param('resources_download', self.resources_download)
		set_param('google_maps_api_key', (self.google_maps_api_key or '').strip())
			

