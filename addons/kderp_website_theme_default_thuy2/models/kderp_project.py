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
	
	def onchange_location(self, cr, uid, ids, project_location_id=False):
		val={}
		if not project_location_id:
			val={
				'area_id': False
			}
		else:
			location = self.pool.get('kderp.location').browse(cr, uid, project_location_id)
			val={
				'area_id': location.area_id.id if location.area_id else False,
			}
		return {'value':val}

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
		'name':fields.char('Name',size=128,required=True),
		'description':fields.char('Description',size=128),
		'area_id':fields.many2one('kderp.area', 'Area'),
		}
kderp_location()

class kderp_area(osv.Model):
	_name = "kderp.area"
	_columns = {
		'code':fields.char('Code', required=True),
		'name':fields.char('Name', translate=True, required = True),
		}
kderp_area()

