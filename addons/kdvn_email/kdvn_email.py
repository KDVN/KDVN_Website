from datetime import datetime

from openerp import tools
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_lead(osv.osv):
	_inherit = 'crm.lead'
	_columns = {}

	def create(self, cr, uid, vals, context=None):
		res = super(crm_lead, self).create(cr, uid, vals, context=context)
		if vals:
			template = self.pool.get('ir.model.data').get_object(cr, uid, 'kdvn_email', 'email_template_auto_contact_us')
			mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, res , force_send=True)
		return res

crm_lead()
class hr_applicant(osv.osv):
	_inherit = 'hr.applicant'
	_columns = {}

	def create(self, cr, uid, vals, context=None):
		res = super(hr_applicant, self).create(cr, uid, vals, context=context)
		if vals:
			template = self.pool.get('ir.model.data').get_object(cr, uid, 'kdvn_email', 'email_template_auto_application')
			mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, res , force_send=True)
		return res

hr_applicant()