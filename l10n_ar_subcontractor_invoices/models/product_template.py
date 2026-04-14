from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    invoiced_by_subcontractor = fields.Boolean(string="Invoiced by subcontractor")
