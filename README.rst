pretix Service Fees
==========================

This is a plugin for `pretix`_.

Features
--------

- **Order-level service fee**: Fixed fee per order, percentual fee per order, and/or fixed fee per ticket (with options to skip free products, add-ons, non-admission products, gift-card-paid amounts).
- **Per-product fee (default)**: Optional default fee per product line (amount and/or percent). Event setting: "Per-product fee (default)" with mode **Add to product price** (fee as separate line) or **Include in product price** (no extra line; customer pays listed price only).
- **Per-product override**: On each product's edit page, **Service fee** section: "Exclude this product from order-level fees" and "Use custom per-product fee" with amount, percent, and mode. Product overrides replace the event default for that product.

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
