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

# Add Date
class hr_job(osv.Model):
	_name = "hr.job"
	_description = "Job Position"
	_inherit = ['hr.job']

	_columns={
		'date_input': fields.date('Date'),
		'date_deadline': fields.date('Deadline'),
	}
	_defaults = {
		'date_input':lambda *a: time.strftime('%Y-%m-%d')
	}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
