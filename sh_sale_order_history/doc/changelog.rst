15.0.1 ( Date : 18 September 2021 )
-----------------------------------

- Initial Release

15.0.2 ( Date : 27 January 2022 )
---------------------------------

[Add] Parent and Child company SO in Sale order history.

[Add] Configuration for Enable Reorder Button For Sales order History


15.0.3 ( Date : 16 February 2022 )
----------------------------------

[ADD] : Date Of Sale order
[Add] : Price According to Pricelist
[Add] : Fixed Product Description

15.0.4 ( Date : 13 April 2022 )
-------------------------------

[Add] Configurations for filter SO By Last Day and Stage data.
[Add] Two buttons for Reorder and view SO, And SO Status field in form and tree view. 

15.0.5 ( Date : 1 September 2022 )
-------------------------------

[Add] New Price and pricelist field display new price from based on pricelist.

15.0.6 ( Date : 10 March 2023 )
-------------------------------

- [REMOVE] - Remove Reload after Reorder.


15.0.7 ( Date : 13 March 2023 )
-----------------------------------

[Add] Display Sale Order History on already created Sale Orders also.



15.0.8 ( Date : 22 Apr 2023 )
-------------------------------

- [fix] Small bug fixed.

sh_sale_order_history/models/sale_order_history.py", line 94, in _compute_new_unit_price
    [(record.product_id, record.product_uom_qty, record.order_id.partner_id,)], uom_id=record.product_uom.id)
odoo/odoo/addons/product/models/product_pricelist.py", line 166, in _compute_price_rule
    items = self._compute_price_rule_get_items(products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids)                                                     ^
HINT:  No operator matches the given name and argument types. You might need to add explicit type casts.

