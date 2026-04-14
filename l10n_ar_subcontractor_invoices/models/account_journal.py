from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoiced_by_subcontractor = fields.Boolean(string="Invoices by subcontractors")
