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
		'project_purpose_id': fields.many2one('kderp.blog.post.project.purpose', string="Purpose of use"),
		'type': fields.many2one('kderp.blog.post.project.type',"Project Type"),
		'size': fields.many2one('kderp.blog.post.project.size',"Project Size"),
		}
		
	def onchange_year(self, cr, uid, ids, completion_date, project_year_id):
		val={}
		cr.execute("""select id, code from kderp_blog_post_year """)
		if not completion_date:
			val={'project_year_id':None}
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
	('kderp_unique_code_blog_post_year','unique(code, name)', 'Blog post year Code, Name must be unique')
kderp_blog_post_year()

class kderp_blog_post_project_type(osv.Model):
	_name = "kderp.blog.post.project.type"

	_columns = {
		'code':fields.char('Code',required=True),
		'name':fields.char('Name',required=True)
		}
	('kderp_unique_code_blog_post_project_type','unique(code, name)', 'Blog post type Code, Name must be unique')
kderp_blog_post_project_type()

class kderp_blog_post_project_size(osv.Model):
	_name = "kderp.blog.post.project.size"

	_columns = {
		'code':fields.char('Code', required=True),
		'name':fields.char('Name', required=True)
		}
	('kderp_unique_code_blog_post_project_size','unique(code, name)', 'Blog post size Code, Name must be unique')
kderp_blog_post_project_size()

class kderp_blog_post_project_purpose(osv.Model):
    _name = 'kderp.blog.post.project.purpose'
    _description = 'Kderp Blog Post Project Purpose'
        
    _columns = {
                'sequence':fields.integer("Seq."),
                'name': fields.char("Name", size=16, required = True, translate=True),
                'description':fields.char("Description", size=128)
                }
    _sql_constraints = [
        ('kderp_unique_sequence_project_purpose','unique(sequence)', 'Project Purpose Name must be unique'),
        ('kderp_unique_name_project_purpose','unique(name)', 'Project Purpose Name must be unique')
        ]

kderp_blog_post_project_purpose()

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
	('kderp_unique_code_area','unique(code, name)', 'Area Code, Name must be unique')
kderp_area()

