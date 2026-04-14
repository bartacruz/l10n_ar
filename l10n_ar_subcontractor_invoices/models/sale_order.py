from odoo import models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_invoiceable_lines(self, final=False):
        lines = super(SaleOrder, self)._get_invoiceable_lines(final=final)
        # for line in self.order_line:
        #     print(
        #         "Line to invoice?",
        #         line.product_id,
        #         line.qty_to_invoice,
        #         line.invoice_status,
        #     )
        return lines
