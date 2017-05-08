# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    
    #Add a boolean check for Instructor
    instructor = fields.Boolean("Instructor", default=False)
    
    session_ids = fields.Many2many('openacademy.session', string='Attended Sessions', readonly=True)