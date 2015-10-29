from openerp import api, models, fields, SUPERUSER_ID
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta
from openerp import tools
    
class event_event(models.Model):
    _inherit = 'event.event'    
    
    @api.one
    @api.constrains('type', 'date_begin', 'date_end')
    def _check_date_overlap(self):
        if self.type and self.date_begin and self.date_end:
            overlaps = self.search_count(['&','|','&',('date_begin', '>', self.date_begin), ('date_begin', '<', self.date_end),
                                          '&',('date_end', '>', self.date_begin), ('date_end', '<', self.date_end),
                                          ('id', '!=', self.id),
                                          ('type', '!=', False),
                                          ('type', '=', self.type.id)
            ])
            overlaps += self.search_count([('id', '!=', self.id),
                                           ('date_begin', '=', self.date_begin),
                                           ('date_end', '=', self.date_end),
                                           ('type', '=', self.type.id)])
            if overlaps:
                raise ValidationError('There already is booking at that time.')
        elif self.type or self.date_begin or self.date_end:
            raise ValidationError('Provide all of booking parameters')

    @api.model
    def get_bookings(self, start, end, types):
        domain  = [
            ('date_begin', '>=', start), 
            ('date_end', '<=', end),
            ('date_begin', '>=', fields.Datetime.now()),
            ('address_id.name','=','KINDEN VIETNAM')
            ]
        if types:
            domain.append(('type', 'in', types))
        bookings = self.search(domain)
        return [{
            'id': b.id,
            'title': str((datetime.strptime(b.date_begin, tools.DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=7)).strftime('%I:%M %p'))+', '+b.name+', '+b.type.name,
            'start': str(datetime.strptime(b.date_begin, tools.DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=7)),
            'end': str(datetime.strptime(b.date_end, tools.DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=7)),
            'editable': False,
        } for b in bookings]

    @api.model
    def add_backend_booking(self, type, start, end):

        booking_id = self.create({
            'type': type,
            'date_begin': start,
            'date_end': end, 
        })

        return booking_id.id

