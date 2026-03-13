pretix Service Fees
==========================

This is a plugin for `pretix`_.

Features
--------

- **Order-level service fee**: Fixed fee per order, percentual fee per order, and/or fixed fee per ticket (with options to skip free products, add-ons, non-admission products, gift-card-paid amounts).
- **Per-product fee (default)**: Optional default fee per product line (amount and/or percent). Event setting: "Per-product fee (default)" with mode **Add to product price** (fee as separate line) or **Include in product price** (no extra line; customer pays listed price only).
- **Per-product override**: On each product's edit page, **Service fee** section: "Exclude this product from order-level fees" and "Use custom per-product fee" with amount, percent, and mode. Product overrides replace the event default for that product.

For plugin developers: per-position fee data
--------------------------------------------

When per-product fees are applied, this plugin stores the **gross fee amount per order position** in the order's ``meta_info`` so other plugins can build exports or reports (e.g. fee by product for the whole event).

**Public API** (use this instead of reading ``meta_info`` directly):

.. code-block:: python

   from pretix_servicefees import get_order_position_fees, META_KEY_POSITION_FEES

   # Get fee per position for one order (position_id -> Decimal)
   fee_by_position = get_order_position_fees(order)

   # Or read the raw dict: order.meta_info[META_KEY_POSITION_FEES]
   # Format: {str(position_id): "2.50", ...}  (only positions with fee > 0)

**When the data is present**: Set on order placement; removed on order change; on order split, only the original order keeps fees for positions that stayed (the new order has no fee data for moved positions). See ``pretix_servicefees.position_fees`` module docstring for the full contract and an event-level aggregation example.

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-servicefees``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``pip install -e .`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------

Copyright 2018 Raphael Michel

Released under the terms of the Apache License 2.0


.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
