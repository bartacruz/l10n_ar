# -*- coding: utf-8 -*-
from odoo import _, models, fields, api
import stdnum.ar
from odoo.exceptions import ValidationError
class ResPartner(models.Model):
    _inherit = 'res.partner'

    dni = fields.Char(string="DNI", help="Argentinian DNI")
    l10n_ar_dni = fields.Char(string="Computed DNI", compute="_compute_dni", store=True)
    needs_manual_dni = fields.Boolean(compute="_compute_dni", store=True)
    
    @api.depends('l10n_latam_identification_type_id','vat','dni')
    def _compute_dni(self):
        for record in self:
            if record.l10n_latam_identification_type_id.l10n_ar_afip_code == '96':
                # The partner has DNI as her main identification. Use that one.
                record.l10n_ar_dni = record.vat
                record.needs_manual_dni = False
            else:
                # Manually added DNI Field
                record.needs_manual_dni = True
                record.l10n_ar_dni = record.dni
                
    @api.constrains('l10n_ar_dni')
    def check_dni(self):
        # The context key 'no_dni_validation' allows you to store/set a DNI number without doing validations.
        # This is for API pushes from external platforms where you have no control over DNI format.
        if self.env.context.get('no_dni_validation'):
            return
        l10n_ar_partners = self.filtered(lambda partner: partner.l10n_ar_dni)
        module = stdnum.ar.dni
        for record in l10n_ar_partners:
            try:
                module.validate(record.l10n_ar_dni)
            except module.InvalidLength:
                raise ValidationError(_('Invalid length for DNI'))
            except module.InvalidFormat:
                raise ValidationError(_('Only numbers allowed for DNI'))
            except Exception as error:
                raise ValidationError(repr(error))
                