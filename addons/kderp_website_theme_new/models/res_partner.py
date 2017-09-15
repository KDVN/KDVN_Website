from openerp.osv import osv, fields
from openerp.addons.website.models.website import urlplus
from openerp import SUPERUSER_ID

class res_partner(osv.Model):
	#TODO: Central management for API keys
	_inherit = 'res.partner'
	
	def google_map_img(self, cr, uid, ids, zoom=10, width=298, height=298, context=None):
		google_map_api_kdvn_key = self.pool.get('website').browse(cr, uid, uid).google_map_api_kdvn_key
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
		'position_x':fields.char('Position X'),
		'position_y':fields.char('Position Y'),
		}
	
	
res_partner()