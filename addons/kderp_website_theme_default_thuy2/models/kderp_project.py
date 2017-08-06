from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
import time
import datetime
class kderp_blog_post_project(osv.Model):
	_inherit = 'blog.post'
	
	_columns = {
		'blog_name': fields.related('blog_id','name', type="char", string='Blog'),
		'project_location_id': fields.many2one('kderp.location', string="Location"),
		'area_id':fields.many2one('kderp.area', string="Area"),
		'city_id':fields.many2one('kderp.city', string="City"),
		'completion_date': fields.date(string='Completion Date'),
		'project_year_id': fields.many2one('kderp.blog.post.year', string="Years"),
		'type': fields.many2one('kderp.blog.post.project.type',"Project Type"),
		'size': fields.many2one('kderp.blog.post.project.size',"Project Size"),
		}
		
	def onchange_year(self, cr, uid, ids, completion_date, project_year_id):
		val={}
		cr.execute("""select id, code from kderp_blog_post_year """)
		if completion_date:
			completion_date= datetime.datetime.strptime(completion_date,"%Y-%m-%d")
			year = completion_date.strftime('%Y')
			for id, code in cr.fetchall():
				if code == year:
					val={'project_year_id':id}
		return {'value':val}
	
	def onchange_location_city(self, cr, uid, ids, project_location_id=False):
		if not project_location_id:
			return {'value': {
				'city_id': False,
				'area_id': False
				}}
		location = self.pool.get('kderp.location').browse(cr, uid, project_location_id)
		return {'value': {
				'city_id': location.city_id.id if location.city_id else False,
				'area_id': location.area_id.id if location.area_id else False,
				
		}}

kderp_blog_post_project()

class kderp_blog_post_year(osv.Model):
	_name = "kderp.blog.post.year"

	_columns = {
		'code':fields.char('Code',size=4,required=True),
		'name':fields.char('Name',size=100,required=True),
		'description':fields.char('Description',size=128),
		}
kderp_blog_post_year()

class kderp_blog_post_project_type(osv.Model):
	_name = "kderp.blog.post.project.type"

	_columns = {
		'code':fields.char('Code',required=True),
		'name':fields.char('Name',required=True)
		}
kderp_blog_post_project_type()

class kderp_blog_post_project_size(osv.Model):
	_name = "kderp.blog.post.project.size"

	_columns = {
		'code':fields.char('Code', required=True),
		'name':fields.char('Name', required=True)
		}
kderp_blog_post_project_size()

from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
import time

class kderp_location(osv.Model):
	_name = "kderp.location"
	
	_columns = {
		'code':fields.char('Code',size=128,required=True),
		'name':fields.char('Name',size=128,required=True),
		'description':fields.char('Description',size=128),
		'city_id':fields.many2one('kderp.city', 'City'),
		'city_code':fields.related('city_id','code',type="char", string='Code City', readonly=1),
		'area_id':fields.many2one('kderp.area', 'Area'),
		}
	def name_get(self, cr, uid, ids, context=None):
		if isinstance(ids, (list, tuple)) and not len(ids):
			return []
		if isinstance(ids, (long, int)):
			ids = [ids]
		reads = self.read(cr, uid, ids, ['name','code'], context=context)
		res = []
		for record in reads:
			name = "%s - %s" % (record['code'],record['name'])
			
			res.append((record['id'], name))
		return res

	def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
		if not args:
			args=[]
		if context is None:
			context={}

		if name:
			name=name.strip()
			ctc_ids = self.search(cr, uid, [('code', '=', name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid,[('name', 'ilike', name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid,[('city', 'ilike', name)] + args, limit=limit, context=context)                
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
kderp_location()

class kderp_area(osv.Model):
	_name = "kderp.area"
	_columns = {
		'code':fields.char('Code', required=True),
		'name':fields.char('Name', translate=True, required = True),
		}
kderp_area()

class kderp_city(osv.Model):
	_name = "kderp.city"
	_columns = {
		'code':fields.char('Code',size=16, required=True),
		'name':fields.char('Name', size=128, translate=True, required = True),
		}
		
	def name_get(self, cr, uid, ids, context=None):
		if isinstance(ids, (list, tuple)) and not len(ids):
			return []
		if isinstance(ids, (long, int)):
			ids = [ids]
		reads = self.read(cr, uid, ids, ['name','code'], context=context)
		res = []
		for record in reads:
			name = "%s - %s" % (record['code'],record['name'])
			
			res.append((record['id'], name))
		return res

	def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
		if not args:
			args=[]
		if context is None:
			context={}

		if name:
			name=name.strip()
			ctc_ids = self.search(cr, uid, [('code', '=', name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid,[('name', 'ilike', name)] + args, limit=limit, context=context)
			if not ctc_ids:
				ctc_ids = self.search(cr, uid,[('city', 'ilike', name)] + args, limit=limit, context=context)                
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
		
	_sql_constraints=[('kderp.city','unique(code)','Code must be unique !')]
	
kderp_city()
