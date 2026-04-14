from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends(
        "invoice_lines.move_id.state",
        "invoice_lines.quantity",
        "qty_received",
        "product_uom_qty",
        "order_id.state",
    )
    def _compute_qty_invoiced(self):
        ret = super(PurchaseOrderLine, self)._compute_qty_invoiced()
        for line in self.filtered(lambda x: x.product_id.invoiced_by_subcontractor):
            qty = 0.0
            for inv_line in line._get_invoice_lines():
                if (
                    inv_line.move_id.state not in ["cancel"]
                    or inv_line.move_id.payment_state == "invoicing_legacy"
                ):
                    if inv_line.move_id.move_type == "out_invoice":
                        qty += inv_line.product_uom_id._compute_quantity(
                            inv_line.quantity, line.product_uom
                        )
                    elif inv_line.move_id.move_type == "out_refund":
                        qty -= inv_line.product_uom_id._compute_quantity(
                            inv_line.quantity, line.product_uom
                        )
            line.qty_invoiced = qty
            if line.order_id.state in ["purchase", "done"]:
                if line.product_id.purchase_method == "purchase":
                    line.qty_to_invoice = line.product_qty - line.qty_invoiced
                else:
                    line.qty_to_invoice = line.qty_received - line.qty_invoiced
            else:
                line.qty_to_invoice = 0
            _logger.info(
                "computed qty invoiced for subcontracted product %s %s %s %s",
                line.name,
                line,
                line.qty_invoiced,
                line.qty_to_invoice,
            )
        return ret
