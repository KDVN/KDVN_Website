# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 OpenSur.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.osv import osv, fields
from openerp.addons.hr_recruitment import hr_recruitment

class hr_department(osv.Model):
	_name = "hr.department"
	_inherit = "hr.department"
	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		reads = self.read(cr, uid, ids, ['code','name'], context=context)
		res = []
		for record in reads:
			name = record['code']
			if record['name']:
				name = "%s - %s" % (name,record['name'])
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
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
		
	_columns={
			'manager_2nd_id':fields.many2one('res.users','2nd Manager'),
			'code':fields.char('Code'),
			}
				   
class kdvn_hr_job_language(osv.Model):
	_name = "kdvn.hr.job.language"
	_description = "Job Preferred Language"
	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		reads = self.read(cr, uid, ids, ['code','name'], context=context)
		res = []
		for record in reads:
			name = record['code']
			if record['name']:
				name = "%s - %s" % (name,record['name'])
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
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
		
	_columns={
		'code':fields.char('Code',size=4,required=True),
		'name': fields.char('Name', size=64, required = True, translate= True),
		'description':fields.char('Description', size=128),
		'jobs_ids': fields.one2many('hr.job', 'job_language_id', 'Jobs'),
	}
class kdvn_hr_job_level(osv.Model):
	_name = "kdvn.hr.job.level"
	_description = "Job Level"
	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		reads = self.read(cr, uid, ids, ['code','name'], context=context)
		res = []
		for record in reads:
			name = record['code']
			if record['name']:
				name = "%s - %s" % (name,record['name'])
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
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
		
	_columns={
		'code':fields.char('Code',size=4,required=True),
		'name': fields.char('Name', size=64, required = True, translate= True),
		'description':fields.char('Description', size=128),
		'jobs_ids': fields.one2many('hr.job', 'job_level_id', 'Jobs'),
	}
class kdvn_hr_job_work_place(osv.Model):
	_name = "kdvn.hr.job.work.place"
	_description = "Job Work Place"
	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		reads = self.read(cr, uid, ids, ['code','name'], context=context)
		res = []
		for record in reads:
			name = record['code']
			if record['name']:
				name = "%s - %s" % (name,record['name'])
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
		else:
			ctc_ids = self.search(cr, uid, args, limit=limit, context=context)
		return self.name_get(cr, uid, ctc_ids, context=context)
		
	_columns={
		'code':fields.char('Code',size=4,required=True),
		'name': fields.char('Name', size=64, required = True, translate= True),
		'description':fields.char('Description', size=128),
		'jobs_ids': fields.one2many('hr.job', 'job_work_place_id', 'Jobs'),
	}
	
class hr_job(osv.Model):
	_name = "hr.job"
	_description = "Job Position"
	_inherit = ['hr.job']
	#Ham tao code HR tu dong
	def new_code(self,cr,uid,ids,department_id,date,code=False):
		if ids:
			try:
				ids=ids[0]
			except:
				ids=ids
		else:
			ids=0
		if (not department_id):
			val={'value':{'code':False}}
		else:	
			staff_code_list=self.pool.get("hr.department").read(cr,uid,department_id,['code'])
			if not staff_code_list:
				val={'value':{'code':False}}
			else:
				staff_code = staff_code_list['code']
				prefix = len('HR17-%s-X' % staff_code)
				cr.execute("Select \
								max(substring(code from "+str(prefix)+" for length(code)-"+str(prefix-1)+"))::integer \
							from \
								hr_job \
							where code ilike 'HR" + date[:4][2:]+"-"+staff_code+"-"+"%%'  and id!="+str(ids))
				if cr.rowcount:
					next_code=str(cr.fetchone()[0])
					if next_code.isdigit():
						next_code=str(int(next_code)+1)
					else:
						next_code= '1'
				else:
					next_code='1'
				
			val={'value':{'code':'HR%s-%s-%s' % (date[:4][2:],staff_code,next_code.rjust(2,'0'))}}	
		return val
		
	_columns={
		'code':fields.char('Code', size=64, required=True, track_visibility='onchange', select=True ),
		'date_input': fields.date('Date'),
		'date_deadline': fields.date('Deadline'),
		'job_language_id': fields.many2one('kdvn.hr.job.language', 'Job language'),
		'job_level_id': fields.many2one('kdvn.hr.job.level', 'Job level'),
		'job_work_place_id': fields.many2one('kdvn.hr.job.work.place', 'Job work place'),
		'job_link': fields.char('Job link'),
		'description': fields.text('Job Description', translate=True),
    	'requirements': fields.text('Requirements', translate=True)
	}
	_sql_constraints = [
		('name_company_uniq', 'unique(code, company_id, department_id)', 'The code of the job position must be unique per department in company!'),
	]
	_defaults = {
		'date_input':lambda *a: time.strftime('%Y-%m-%d')
	}
	
class hr_applicant(osv.Model):
	_name = "hr.applicant"
	_inherit = ['hr.applicant']
	_columns={
		'priority': fields.selection(hr_recruitment.AVAILABLE_PRIORITIES, 'Appreciation'),
	}
	_defaults = {
		'priority': lambda *a: hr_recruitment.AVAILABLE_PRIORITIES[2][0],
		}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
