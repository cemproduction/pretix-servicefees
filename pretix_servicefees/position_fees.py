"""
Per-position service fee data for use by other plugins (exports, reports, analytics).

This module documents and exposes the contract for the per-product service fee amounts
stored on each order so that other plugins can reliably read and aggregate fee data
without depending on implementation details.

Storage (Option A: order metadata)
----------------------------------

When the pretix-servicefees plugin is active and per-product fees are applied, it
stores the **gross fee amount per order position** in the order's meta_info so that:

- No extra database table is used.
- Data is loaded with the order (no extra query).
- Event-level reports can aggregate fee by product by iterating orders and positions.

Key and format
--------------

- **Key**: ``order.meta_info["servicefees_position_fees"]``
- **Constant**: Use ``META_KEY_POSITION_FEES`` from this module for the key name.
- **Value**: A dict mapping **position id (string)** to **gross fee amount (string)**.
  - Keys: ``str(position.id)`` for each order position that had a non-zero per-product fee.
  - Values: fee in order currency, as string (e.g. ``"2.50"``) for JSON compatibility.

When the data is present
------------------------

- Set on **order_placed**: only when the order was created through the normal flow
  and the number of positions matched the fee calculation. Orders created via API
  or bulk import may not have this key.
- **order_changed**: The key is removed when the order or its positions are changed
  (we cannot recompute per-position fees for "included" mode after the fact).
- **order_split**: The original order keeps only fees for positions that remained;
  the new (split) order does not get fee data for the moved positions (no mapping
  from old to new position ids).

Example: event-level fee report by product
------------------------------------------

.. code-block:: python

    from decimal import Decimal
    from pretix_servicefees.position_fees import get_order_position_fees, META_KEY_POSITION_FEES

    # Single order: get fee per position
    fee_by_position = get_order_position_fees(order)
    # -> {position_id: Decimal("2.50"), ...}  (only positions with fee > 0)

    # Event-level: aggregate fee by product (item)
    from pretix.base.models import Order

    orders = Order.objects.filter(event=event).prefetch_related("positions", "positions__item")
    fee_by_item = {}  # item_id -> total fee
    for order in orders:
        fees = get_order_position_fees(order)
        for pos in order.positions.all():
            amt = fees.get(pos.id)
            if amt is not None and amt > 0:
                fee_by_item[pos.item_id] = fee_by_item.get(pos.item_id, Decimal("0")) + amt
"""

from decimal import Decimal
from typing import Dict, Optional

# Public constant: key in order.meta_info for the per-position fee dict.
# Other plugins should use this constant instead of hardcoding the string.
META_KEY_POSITION_FEES = "servicefees_position_fees"


def get_order_position_fees(order) -> Dict[int, Decimal]:
    """
    Return the per-position service fee amounts for an order (for use by other plugins).

    Args:
        order: A pretix Order instance (with meta_info; positions need not be prefetched).

    Returns:
        A dict mapping **position id (int)** to **gross fee (Decimal)**. Only positions
        with a non-zero per-product fee are included. If the order has no stored data,
        an empty dict is returned.

    Example:
        fee_by_position = get_order_position_fees(order)
        for position in order.positions.all():
            fee = fee_by_position.get(position.id) or Decimal("0")
            # use position.item_id, position.price, fee for reports
    """
    if not order.meta_info:
        return {}
    raw = order.meta_info.get(META_KEY_POSITION_FEES)
    if not raw or not isinstance(raw, dict):
        return {}
    result = {}
    for pid_str, amount_str in raw.items():
        try:
            pid = int(pid_str)
            amount = Decimal(amount_str)
            if amount > 0:
                result[pid] = amount
        except (TypeError, ValueError):
            continue
    return result
