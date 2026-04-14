from odoo import models
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_to_invoice_qty(self):
        """
        Compute the quantity to invoice. If the invoice policy is order, the quantity to invoice is
        calculated from the ordered quantity. Otherwise, the quantity delivered is used.
        """
        for line in self:
            if line.product_id.invoiced_by_subcontractor:
                # Don't include this line in the sale order invoice
                _logger.info(
                    "SaleOrderLine %s is subcontracted: setting qty_to_invoice=0", line
                )
                line.qty_to_invoice = 0
        return super(SaleOrderLine, self)._get_to_invoice_qty()
